import argparse
import os
import sys
from dotenv import load_dotenv
from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings
from typing import Literal


# ========== 环境加载诊断日志（已禁用） ==========
# def _print_env_debug(stage: str, message: str):
#     """打印环境加载调试信息"""
#     print(f"[ENV-DEBUG][{stage}] {message}", flush=True)


class AppSettings(BaseSettings):
    """
    应用配置
    """

    app_env: str = 'dev'
    app_name: str = 'CaseGo'
    # app_root_path: str = '/dev-api'
    app_root_path: str = '/'
    app_host: str = '0.0.0.0'
    app_port: int = 9099
    app_version: str = '1.0.0'
    app_reload: bool = False
    app_ip_location_query: bool = True
    app_same_time_login: bool = False
    app_workers: int = 3


class JwtSettings(BaseSettings):
    """
    Jwt配置
    """

    jwt_secret_key: str = 'b01c66dc2c58dc6a0aabfe21442)78bf87f72c0c795dda67f4d55'
    jwt_algorithm: str = 'HS256'
    jwt_expire_minutes: int = 1440
    jwt_redis_expire_minutes: int = 30


class DataBaseSettings(BaseSettings):
    """
    数据库配置
    """

    db_type: Literal['mysql', 'postgresql'] = 'postgresql'
    db_host: str = '127.0.0.1'
    db_port: int = 5432
    db_username: str = 'postgres'
    db_password: str = '123456'
    db_database: str = 'postgres'
    db_echo: bool = False
    db_max_overflow: int = 20
    db_pool_size: int = 10
    db_pool_recycle: int = 3600
    db_pool_timeout: int = 30

    @computed_field
    @property
    def sqlglot_parse_dialect(self) -> str:
        if self.db_type == 'postgresql':
            return 'postgres'
        return self.db_type


class RedisSettings(BaseSettings):
    """
    Redis配置
    """

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_username: str = ''
    redis_password: str = '123456'
    redis_database: int = 1


class LLMSettings(BaseSettings):
    """
    Redis配置
    """

    TAVILY_API_KEY: str = 'tvly-dev-'
    LANGSMITH_API_KEY: str = 'lsv2_pt_'
    LANGSMITH_TRACING: bool = True

    LANGSMITH_PROJECT: str = 'demo'


class GenSettings:
    """
    代码生成配置
    """

    author = 'david'
    package_name = 'module_admin.system'
    auto_remove_pre = False
    table_prefix = 'sys_'
    allow_overwrite = False

    GEN_PATH = 'CaseGo/gen_path'

    def __init__(self):
        if not os.path.exists(self.GEN_PATH):
            os.makedirs(self.GEN_PATH)


class UploadSettings:
    """
    上传配置
    """

    UPLOAD_PREFIX = '/profile'
    UPLOAD_PATH = 'CaseGo/upload_path'
    UPLOAD_MACHINE = 'A'
    DEFAULT_ALLOWED_EXTENSION = [
        # 图片
        'bmp',
        'gif',
        'jpg',
        'jpeg',
        'png',
        # word excel powerpoint
        'doc',
        'docx',
        'xls',
        'xlsx',
        'ppt',
        'pptx',
        'html',
        'htm',
        'txt',
        # 压缩文件
        'rar',
        'zip',
        'gz',
        'bz2',
        # 视频格式
        'mp4',
        'avi',
        'rmvb',
        # pdf
        'pdf',
    ]
    DOWNLOAD_PATH = 'CaseGo/download_path'

    def __init__(self):
        if not os.path.exists(self.UPLOAD_PATH):
            os.makedirs(self.UPLOAD_PATH)
        if not os.path.exists(self.DOWNLOAD_PATH):
            os.makedirs(self.DOWNLOAD_PATH)


class CachePathConfig:
    """
    缓存目录配置
    """

    PATH = os.path.join(os.path.abspath(os.getcwd()), 'caches')
    PATHSTR = 'caches'


class GetConfig:
    """
    获取配置
    """

    def __init__(self):
        self.parse_cli_args()

    @lru_cache()
    def get_app_config(self):
        """
        获取应用配置
        """
        # 实例化应用配置模型
        return AppSettings()

    @lru_cache()
    def get_jwt_config(self):
        """
        获取Jwt配置
        """
        # 实例化Jwt配置模型
        return JwtSettings()

    @lru_cache()
    def get_database_config(self):
        """
        获取数据库配置
        """
        # 实例化数据库配置模型
        return DataBaseSettings()

    @lru_cache()
    def get_redis_config(self):
        """
        获取Redis配置
        """
        # 实例化Redis配置模型
        return RedisSettings()

    @lru_cache()
    def get_gen_config(self):
        """
        获取代码生成配置
        """
        # 实例化代码生成配置
        return GenSettings()

    @lru_cache()
    def get_upload_config(self):
        """
        获取数据库配置
        """
        # 实例上传配置
        return UploadSettings()

    @lru_cache()
    def get_llm_config(self):
        """
        获取数据库配置
        """
        # 实例上传配置
        return LLMSettings()

    @staticmethod
    def parse_cli_args():
        """
        解析命令行参数
        """
        # _print_env_debug("INIT", "=" * 60)
        # _print_env_debug("INIT", "开始解析环境配置")
        # _print_env_debug("INIT", f"当前工作目录: {os.getcwd()}")
        # _print_env_debug("INIT", f"sys.argv: {sys.argv}")

        if 'uvicorn' in sys.argv[0]:
            # 使用uvicorn启动时，命令行参数需要按照uvicorn的文档进行配置，无法自定义参数
            # _print_env_debug("CLI", "检测到 uvicorn 启动模式，跳过命令行参数解析")
            pass
        else:
            # 使用argparse定义命令行参数
            parser = argparse.ArgumentParser(description='命令行参数')
            parser.add_argument('--env', type=str, default='', help='运行环境')
            # 解析命令行参数
            args = parser.parse_args()
            # 设置环境变量，如果未设置命令行参数，默认APP_ENV为dev
            os.environ['APP_ENV'] = args.env if args.env else 'dev'
            # _print_env_debug("CLI", f"命令行参数 --env: {args.env}")

        # 打印启动前的关键环境变量
        # _print_env_debug("ENV-BEFORE", f"APP_ENV (shell): {os.environ.get('APP_ENV', '<未设置>')}")
        # _print_env_debug("ENV-BEFORE", f"APP_PORT (shell): {os.environ.get('APP_PORT', '<未设置>')}")
        # _print_env_debug("ENV-BEFORE", f"APP_WORKERS (shell): {os.environ.get('APP_WORKERS', '<未设置>')}")
        # _print_env_debug("ENV-BEFORE", f"DB_HOST (shell): {os.environ.get('DB_HOST', '<未设置>')}")
        # _print_env_debug("ENV-BEFORE", f"REDIS_HOST (shell): {os.environ.get('REDIS_HOST', '<未设置>')}")

        # 读取运行环境
        run_env = os.environ.get('APP_ENV', '')
        # 运行环境未指定时默认加载.env.dev
        env_file = '.env.dev'
        # 运行环境不为空时按命令行参数加载对应.env文件
        if run_env != '':
            env_file = f'.env.{run_env}'

        # 检查文件是否存在
        # env_file_path = os.path.join(os.getcwd(), env_file)
        # env_file_exists = os.path.exists(env_file_path)
        # _print_env_debug("FILE", f"尝试加载配置文件: {env_file}")
        # _print_env_debug("FILE", f"配置文件完整路径: {env_file_path}")
        # _print_env_debug("FILE", f"配置文件是否存在: {env_file_exists}")

        # 加载配置
        load_dotenv(env_file, override=False)
        # _print_env_debug("LOAD", f"load_dotenv 返回值: {load_result}")

        # 打印加载后的关键环境变量
        # _print_env_debug("ENV-AFTER", f"APP_ENV: {os.environ.get('APP_ENV', '<未设置>')}")
        # _print_env_debug("ENV-AFTER", f"APP_PORT: {os.environ.get('APP_PORT', '<未设置>')}")
        # _print_env_debug("ENV-AFTER", f"APP_WORKERS: {os.environ.get('APP_WORKERS', '<未设置>')}")
        # _print_env_debug("ENV-AFTER", f"APP_SAME_TIME_LOGIN: {os.environ.get('APP_SAME_TIME_LOGIN', '<未设置>')}")
        # _print_env_debug("ENV-AFTER", f"DB_HOST: {os.environ.get('DB_HOST', '<未设置>')}")
        # _print_env_debug("ENV-AFTER", f"DB_PORT: {os.environ.get('DB_PORT', '<未设置>')}")
        # _print_env_debug("ENV-AFTER", f"REDIS_HOST: {os.environ.get('REDIS_HOST', '<未设置>')}")
        # _print_env_debug("INIT", "=" * 60)


# 实例化获取配置类
get_config = GetConfig()
# 应用配置
AppConfig = get_config.get_app_config()
# Jwt配置
JwtConfig = get_config.get_jwt_config()
# 数据库配置
DataBaseConfig = get_config.get_database_config()
# Redis配置
RedisConfig = get_config.get_redis_config()
# 代码生成配置
GenConfig = get_config.get_gen_config()
# 上传配置
UploadConfig = get_config.get_upload_config()

LLMConfig = get_config.get_llm_config()
# ========== 打印最终加载的配置（已禁用） ==========
# _print_env_debug("CONFIG", "=" * 60)
# _print_env_debug("CONFIG", "Pydantic BaseSettings 最终加载的配置值:")
# _print_env_debug("CONFIG", f"AppConfig.app_env: {AppConfig.app_env}")
# _print_env_debug("CONFIG", f"AppConfig.app_port: {AppConfig.app_port}")
# _print_env_debug("CONFIG", f"AppConfig.app_workers: {AppConfig.app_workers}")
# _print_env_debug("CONFIG", f"AppConfig.app_same_time_login: {AppConfig.app_same_time_login}")
# _print_env_debug("CONFIG", f"DataBaseConfig.db_host: {DataBaseConfig.db_host}")
# _print_env_debug("CONFIG", f"DataBaseConfig.db_port: {DataBaseConfig.db_port}")
# _print_env_debug("CONFIG", f"DataBaseConfig.db_database: {DataBaseConfig.db_database}")
# _print_env_debug("CONFIG", f"RedisConfig.redis_host: {RedisConfig.redis_host}")
# _print_env_debug("CONFIG", f"RedisConfig.redis_port: {RedisConfig.redis_port}")
# _print_env_debug("CONFIG", "=" * 60)
