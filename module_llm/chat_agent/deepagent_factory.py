# -*- coding: utf-8 -*-
"""
DeepAgent 工厂 - 创建配置完整的 deep agent

职责：
  1. 使用 create_deep_agent 替代原有的 LangGraph create_graph
  2. 集成模型、工具、MCP、文件系统、Skills
  3. 支持用户/会话级隔离
"""
import os
import re
import subprocess
from urllib.parse import quote_plus

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, LocalShellBackend
from deepagents.backends.protocol import ExecuteResponse, FileDownloadResponse
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
import asyncio

from config.env import DataBaseConfig
from module_llm.chat_agent.subagents import build_search_subagent
from utils.log_util import logger

# 默认系统提示词（模块加载时读取一次）
_DEFAULT_SYSTEM_PROMPT: str | None = None


def _load_default_system_prompt() -> str:
    """从 prompts/default_system_prompt.txt 加载默认系统提示词"""
    global _DEFAULT_SYSTEM_PROMPT
    if _DEFAULT_SYSTEM_PROMPT is not None:
        return _DEFAULT_SYSTEM_PROMPT
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "default_system_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            _DEFAULT_SYSTEM_PROMPT = f.read().strip()
        logger.info(f"加载默认系统提示词: {prompt_path} ({len(_DEFAULT_SYSTEM_PROMPT)} chars)")
    except FileNotFoundError:
        logger.warning(f"默认系统提示词文件不存在: {prompt_path}，使用内置兜底")
        _DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
    return _DEFAULT_SYSTEM_PROMPT


class _WindowsCompatShellBackend(LocalShellBackend):
    """跨平台兼容 Shell 后端。

    修复以下问题：
    1. download_files (rb) 与 edit (r) 换行符不一致（Windows 特有）：
       download_files 以 rb 模式读取保留 \\r\\n，edit 以 r 模式自动转 \\n，
       导致 SummarizationMiddleware 做字符串替换时匹配失败。
    2. virtual_mode=True 时虚拟路径与 shell 命令不兼容（跨平台）：
       文件操作返回虚拟路径（如 /script.py），LLM 在 shell 命令中使用该路径，
       - Windows 将 / 解析为当前驱动器根目录（如 D:\\）
       - Linux 将 /script.py 解析为文件系统根目录
       两种情况均会导致找不到文件，需统一转换为真实工作区路径。
    """

    def download_files(self, paths: list[str]) -> list[FileDownloadResponse]:
        responses = super().download_files(paths)
        for resp in responses:
            if resp.content is not None and resp.error is None:
                resp.content = resp.content.replace(b"\r\n", b"\n")
        return responses

    def _resolve_virtual_to_real(self, virtual_path: str) -> str | None:
        """尝试将虚拟路径解析为工作区内的真实路径。

        复用父类 _resolve_path（库自带的虚拟路径→真实路径解析），
        如果解析后的路径（或其父目录）确实存在于工作区内，返回真实绝对路径；
        否则返回 None，表示该路径不属于工作区（可能是系统路径如 /usr/bin）。
        """
        try:
            resolved = self._resolve_path(virtual_path)
            # 文件或目录本身存在
            if resolved.exists():
                return str(resolved)
            # 父目录存在（支持即将创建的文件，如 echo "x" > /subdir/new.py）
            if resolved.parent != self.cwd and resolved.parent.exists():
                return str(resolved)
        except (ValueError, OSError):
            pass
        return None

    def _convert_virtual_paths(self, command: str) -> str:
        """将命令中的虚拟路径转换为工作区真实路径（跨平台）。

        virtual_mode=True 时，LLM 使用形如 /filename.py 的虚拟路径，
        需替换为工作区内的真实绝对路径。

        转换策略（复用库自带的 _resolve_path，无需硬编码系统路径排除列表）：
        - 用 _resolve_path 将虚拟路径解析为工作区内真实路径
        - 如果解析后的文件/目录（或其父目录）存在 → 替换为真实路径
        - 如果 _resolve_path 抛出异常或解析后不存在 → 保持原样（系统路径）
        """
        if not self.virtual_mode:
            return command

        def _replace_path(match: re.Match) -> str:
            prefix = match.group(1)   # 前置分隔符（空白/引号/等号）
            path = match.group(2)     # /filename 部分
            real = self._resolve_virtual_to_real(path)
            if real is not None:
                return f'{prefix}{real.replace(chr(92), "/")}'
            return match.group(0)

        # 替换：空白/引号/等号后紧跟 /字母或下划线 开头的路径
        command = re.sub(
            r'([\s"\'=])(/[a-zA-Z_][^\s"\']*)',
            _replace_path,
            command,
        )

        # 替换：命令以 /path 开头的情况
        def _replace_leading_path(match: re.Match) -> str:
            path = match.group(0)
            real = self._resolve_virtual_to_real(path)
            if real is not None:
                return real.replace(chr(92), '/')
            return path

        command = re.sub(r'^(/[a-zA-Z_][^\s"\']*)', _replace_leading_path, command)

        return command

    def execute(self, command: str, *, timeout: int | None = None) -> ExecuteResponse:
        """执行 shell 命令，包含跨平台兼容性修复。

        修复内容：
        1. 虚拟路径转换（跨平台）：virtual_mode=True 时 /script.py → 真实工作区路径
        2. stdin 重定向：防止子进程等待 stdin 输入导致挂起
        3. 隐藏控制台窗口（Windows）：防止弹出 cmd 窗口
        """
        # 虚拟路径转换（跨平台，不再限制 Windows）
        command = self._convert_virtual_paths(command)

        # 参数校验
        if not command or not isinstance(command, str):
            return ExecuteResponse(
                output="Error: Command must be a non-empty string.",
                exit_code=1,
                truncated=False,
            )

        effective_timeout = timeout if timeout is not None else self._default_timeout
        if effective_timeout <= 0:
            msg = f"timeout must be positive, got {effective_timeout}"
            raise ValueError(msg)

        try:
            run_kwargs = dict(
                check=False,
                shell=True,
                capture_output=True,
                encoding='utf-8',   # 强制 UTF-8，避免 Windows 默认 GBK 解码崩溃
                errors='replace',   # 无法解码的字节用 ? 替代，不抛异常
                timeout=effective_timeout,
                env=self._env,
                cwd=str(self.cwd),
                stdin=subprocess.DEVNULL,  # 防止子进程等待 stdin 导致挂起
            )
            # Windows: 隐藏控制台窗口
            if os.name == 'nt':
                run_kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(command, **run_kwargs)  # noqa: S602

            # 合并 stdout 和 stderr
            output_parts = []
            if result.stdout:
                output_parts.append(result.stdout)
            if result.stderr:
                stderr_lines = result.stderr.strip().split("\n")
                output_parts.extend(f"[stderr] {line}" for line in stderr_lines)

            output = "\n".join(output_parts) if output_parts else "<no output>"

            # 输出截断检查
            truncated = False
            if len(output) > self._max_output_bytes:
                output = output[: self._max_output_bytes]
                output += f"\n\n... Output truncated at {self._max_output_bytes} bytes."
                truncated = True

            # 非零退出码追加提示
            if result.returncode != 0:
                output = f"{output.rstrip()}\n\nExit code: {result.returncode}"

            return ExecuteResponse(
                output=output,
                exit_code=result.returncode,
                truncated=truncated,
            )

        except subprocess.TimeoutExpired:
            if timeout is not None:
                msg = f"Error: Command timed out after {effective_timeout} seconds (custom timeout). The command may be stuck or require more time."
            else:
                msg = f"Error: Command timed out after {effective_timeout} seconds. For long-running commands, re-run using the timeout parameter."
            return ExecuteResponse(output=msg, exit_code=124, truncated=False)
        except Exception as e:  # noqa: BLE001
            return ExecuteResponse(
                output=f"Error executing command ({type(e).__name__}): {e}",
                exit_code=1,
                truncated=False,
            )

# 全局工作区根目录（与原 UserThreadFilesystemBackend 保持一致）
WORKSPACE_ROOT = os.path.join("CaseGo", "agent_workspace")

# 共享技能目录（全用户可读，不受用户隔离限制）
SKILLS_ROOT = os.path.join("CaseGo", "skills")


def _get_postgres_uri() -> str:
    """构建 PostgreSQL 连接字符串（psycopg3 格式）"""
    return (
        f"postgresql://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@"
        f"{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}"
    )


# 模块级连接池和 checkpointer，应用生命周期内复用
_pool: AsyncConnectionPool | None = None
_checkpointer: AsyncPostgresSaver | None = None
_init_lock = asyncio.Lock()


async def get_checkpointer() -> AsyncPostgresSaver:
    """获取全局 AsyncPostgresSaver 实例（懒初始化）"""
    global _pool, _checkpointer
    if _checkpointer is not None:
        return _checkpointer
    async with _init_lock:
        if _checkpointer is None:
            pool = AsyncConnectionPool(conninfo=_get_postgres_uri(), open=False)
            await pool.open()
            checkpointer = AsyncPostgresSaver(conn=pool)
            await checkpointer.setup()
            _pool = pool
            _checkpointer = checkpointer
    return _checkpointer


async def close_resources():
    """关闭连接池，应用退出时调用"""
    global _pool, _checkpointer
    if _pool is not None:
        await _pool.close()
        _pool = None
        _checkpointer = None


async def create_deep_agent_instance(
        model,
        system_prompt: str = None,
        user_id: int = None,
        thread_id: str = None,
        tools: list = None,
        skills_paths: list[str] = None,
        enable_subagent_mcp: bool = False,
):
    """
    创建配置完整的 deep agent

    :param model: LangChain ChatModel 实例（由 model_factory 创建）
    :param system_prompt: 系统提示词
    :param user_id: 当前用户 ID（用于文件系统隔离）
    :param thread_id: 当前会话 Thread ID
    :param tools: 工具列表（包含内置工具、MCP 工具等）
    :param skills_paths: Skills 目录路径列表
    :param enable_subagent_mcp: 是否为子 Agent 启用 MCP 工具（默认 False，避免浏览器状态问题）
    :return: 编译后的 deep agent
    """
    # 未传入 system_prompt 时，自动加载默认提示词
    if not system_prompt:
        system_prompt = _load_default_system_prompt()

    checkpointer = await get_checkpointer()

    # 配置 Backend：混合文件系统 + 共享技能 + Shell 执行
    def make_backend(runtime):
        # 用户/会话隔离的工作目录
        workspace_root = os.path.join(
            WORKSPACE_ROOT,
            str(user_id),
            str(thread_id)
        )
        os.makedirs(workspace_root, exist_ok=True)

        # 使用 LocalShellBackend 提供文件系统 + execute 工具
        # root_dir 设置为用户隔离目录，virtual_mode=True 防止路径逃逸
        shell_backend = _WindowsCompatShellBackend(
            root_dir=workspace_root,
            virtual_mode=True,
            timeout=120,  # 命令超时 120 秒
            max_output_bytes=100000,  # 最大输出 100KB
            inherit_env=True,  # 继承宿主环境变量（PATH 等），使 python 等命令可用
        )

        # 共享技能目录：所有用户可读，通过 /skills/ 虚拟路径访问
        skills_backend = FilesystemBackend(
            root_dir=SKILLS_ROOT,
            virtual_mode=True,
        )

        return CompositeBackend(
            default=shell_backend,
            routes={
                "/skills/": skills_backend,
            },
        )

    # 分离 MCP 工具和非 MCP 工具
    mcp_tools = []
    non_mcp_tools = []
    for tool in (tools or []):
        tool_name = getattr(tool, 'name', '')
        # MCP 工具通常以特定前缀命名，或者来自 langchain_mcp_adapters
        tool_module = getattr(tool, '__module__', '')
        is_mcp_tool = (
                tool_name.startswith(('browser_', 'fetch_', 'playwright_', 'mcp_'))
                or 'langchain_mcp' in tool_module
                or 'mcp_adapters' in tool_module
        )
        if is_mcp_tool:
            mcp_tools.append(tool)
        else:
            non_mcp_tools.append(tool)

    # 配置子 Agent 列表
    subagents = []

    # 1. 搜索子 Agent：始终注册，使主 Agent 无论是否开启联网搜索都能委派搜索任务
    search_subagent = build_search_subagent(model=model)
    subagents.append(search_subagent)
    logger.info("注册子 Agent: search-agent（联网搜索）")

    # 2. 如果有 MCP 工具且不启用子 Agent MCP，覆盖 general-purpose 子 Agent
    if not enable_subagent_mcp and mcp_tools:
        subagents.append({
            "name": "general-purpose",
            "description": "General-purpose agent for research and multi-step tasks",
            "system_prompt": system_prompt,
            "tools": non_mcp_tools,  # 只包含非 MCP 工具
            "model": model,
        })
        logger.info(
            f"配置 general-purpose 子 Agent: 移除 {len(mcp_tools)} 个 MCP 工具，"
            f"保留 {len(non_mcp_tools)} 个非 MCP 工具"
        )

    # 创建 deep agent
    agent = create_deep_agent(
        model=model,
        system_prompt=system_prompt,
        tools=tools or [],  # 主 Agent 使用全部工具
        skills=skills_paths or [],
        backend=make_backend,
        checkpointer=checkpointer,
        subagents=subagents or None,  # 配置子 Agent（空列表时传 None 使用默认）
        name=f"agent-user{user_id}-thread{thread_id}",
    )

    logger.info(
        f"创建 deep agent: user_id={user_id}, thread_id={thread_id}, "
        f"tools={len(tools or [])}, skills={len(skills_paths or [])}"
    )

    return agent
