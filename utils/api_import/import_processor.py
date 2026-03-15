#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : fast_api_admin
@File    : import_processor.py
@Author  : Claude
@Date    : 2025-12-05
@Description : OpenAPI 导入处理器
支持解析、预览、对比、导入完整流程
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from config.enums import Request_method, Request_Type
from module_admin.api_project_submodules.entity.do.project_submodules_do import ApiProjectSubmodules
from module_admin.api_testing.api_test_cases.entity.do.test_cases_do import ApiTestCases
from module_admin.api_testing.api_headers.entity.do.headers_do import ApiHeaders
from module_admin.api_testing.api_params.entity.do.params_do import ApiParams
from module_admin.api_testing.api_cookies.entity.do.cookies_do import ApiCookies
from module_admin.api_testing.api_formdata.entity.do.formdata_do import ApiFormdata
from module_admin.api_testing.api_assertions.entity.do.assertions_do import ApiAssertions
from module_admin.api_testing.api_setup.entity.do.setup_do import ApiSetup
from module_admin.api_testing.api_teardown.entity.do.teardown_do import ApiTeardown

from utils.api_import.import_openapi import (
    import_openapi,
    OpenAPIParseResult,
    OpenAPIRequestModel,
    OpenAPIFilterConfig
)


# ==================== 枚举类型 ====================

class ModuleStrategy(str, Enum):
    """模块处理策略"""
    AUTO_MATCH = "auto_match"      # 自动匹配已有模块，不存在则创建
    CREATE_ALL = "create_all"      # 全部创建新模块
    TARGET_ONLY = "target_only"    # 只导入到指定的目标模块


class ConflictStrategy(str, Enum):
    """接口冲突处理策略"""
    SKIP = "skip"                  # 跳过已存在的接口
    OVERWRITE = "overwrite"        # 完全覆盖（删除原有数据后新增）
    SMART_MERGE = "smart_merge"    # 智能合并（保留断言、前置、后置）


class ItemStatus(str, Enum):
    """项目状态"""
    NEW = "new"                    # 新增
    MATCH = "match"                # 匹配到已有（需要更新）
    SKIP = "skip"                  # 跳过


# ==================== 配置模型 ====================

class ImportConfig(BaseModel):
    """导入配置"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # 目标配置
    project_id: int = Field(description='目标项目ID')
    target_module_id: Optional[int] = Field(default=None, description='目标父模块ID，None表示一级模块')

    # 模块处理策略
    module_strategy: ModuleStrategy = Field(
        default=ModuleStrategy.AUTO_MATCH,
        description='模块处理策略'
    )

    # 接口冲突处理策略
    conflict_strategy: ConflictStrategy = Field(
        default=ConflictStrategy.SMART_MERGE,
        description='接口冲突处理策略'
    )

    # 导入选项
    import_headers: bool = Field(default=True, description='是否导入headers')
    import_params: bool = Field(default=True, description='是否导入params')
    import_body: bool = Field(default=True, description='是否导入请求体')
    import_cookies: bool = Field(default=True, description='是否导入cookies')
    include_deprecated: bool = Field(default=False, description='是否包含已废弃接口')

    # OpenAPI 过滤配置
    allowed_methods: Optional[List[str]] = Field(default=None, description='允许的HTTP方法')
    include_tags: Optional[List[str]] = Field(default=None, description='只包含的标签')
    exclude_tags: Optional[List[str]] = Field(default=None, description='排除的标签')
    path_patterns: Optional[List[str]] = Field(default=None, description='路径正则匹配')


class ImportExecuteConfig(ImportConfig):
    """执行导入的配置（包含用户选择）"""
    # 用户选择要导入的项
    selected_modules: Optional[List[str]] = Field(
        default=None,
        description='选中的模块名称列表，None表示全选'
    )
    selected_apis: Optional[List[str]] = Field(
        default=None,
        description='选中的接口标识列表（格式: module_name::api_name::method），None表示全选'
    )


# ==================== 预览数据模型 ====================

class PreviewApiItem(BaseModel):
    """预览接口项"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    case_id: Optional[int] = Field(default=None, description='用例ID（新增时为None）')
    name: str = Field(description='接口名称')
    method: str = Field(description='请求方法')
    path: str = Field(description='请求路径')
    type: str = Field(default="api", description='类型')
    status: ItemStatus = Field(default=ItemStatus.NEW, description='状态')
    matched_case_id: Optional[int] = Field(default=None, description='匹配到的用例ID')
    changes: List[str] = Field(default=[], description='变更字段列表')
    children: List[Any] = Field(default=[], description='子节点')
    count: int = Field(default=0, description='子节点数量')

    # 原始数据（用于导入）
    request_type: Optional[Request_Type] = Field(default=None)
    json_data: Optional[Any] = Field(default=None)
    headers: List[Dict] = Field(default=[])
    params: List[Dict] = Field(default=[])
    cookies: List[Dict] = Field(default=[])
    formdata: List[Dict] = Field(default=[])
    description: Optional[str] = Field(default=None)


class PreviewModuleItem(BaseModel):
    """预览模块项"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    module_id: Optional[int] = Field(default=None, description='模块ID（新增时为None）')
    name: str = Field(description='模块名称')
    type: str = Field(default="module", description='类型')
    status: ItemStatus = Field(default=ItemStatus.NEW, description='状态')
    matched_module_id: Optional[int] = Field(default=None, description='匹配到的模块ID')
    children: List[Any] = Field(default=[], description='子模块')
    test_cases: List[PreviewApiItem] = Field(default=[], description='接口列表')
    count: int = Field(default=0, description='接口数量')


class PreviewInfo(BaseModel):
    """预览信息"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str = Field(description='API标题')
    version: str = Field(description='API版本')
    openapi_version: str = Field(description='OpenAPI规范版本')
    description: Optional[str] = Field(default=None, description='描述')
    total_modules: int = Field(description='模块总数')
    total_apis: int = Field(description='接口总数')
    new_modules: int = Field(default=0, description='新增模块数')
    new_apis: int = Field(default=0, description='新增接口数')
    update_apis: int = Field(default=0, description='更新接口数')


class PreviewResult(BaseModel):
    """预览结果"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    code: int = Field(default=200)
    msg: str = Field(default="解析成功")
    success: bool = Field(default=True)
    time: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any] = Field(default={})


# ==================== 导入结果模型 ====================

class ImportResultDetail(BaseModel):
    """导入结果详情"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    modules_created: int = Field(default=0, description='创建的模块数')
    apis_created: int = Field(default=0, description='创建的接口数')
    apis_updated: int = Field(default=0, description='更新的接口数')
    apis_skipped: int = Field(default=0, description='跳过的接口数')
    errors: List[str] = Field(default=[], description='错误信息列表')


class ImportResult(BaseModel):
    """导入结果"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    code: int = Field(default=200)
    msg: str = Field(default="导入成功")
    success: bool = Field(default=True)
    time: datetime = Field(default_factory=datetime.now)
    data: ImportResultDetail = Field(default_factory=ImportResultDetail)


# ==================== 核心函数 ====================

def parse_to_preview(
    source: str,
    config: ImportConfig
) -> PreviewResult:
    """
    解析 OpenAPI 为预览结构（不涉及数据库）

    Args:
        source: OpenAPI 规范的 URL 或文件路径
        config: 导入配置

    Returns:
        PreviewResult: 预览结果
    """
    try:
        # 构建过滤配置
        filter_config = OpenAPIFilterConfig(
            allowed_methods=config.allowed_methods,
            include_tags=config.include_tags,
            exclude_tags=config.exclude_tags,
            path_patterns=config.path_patterns,
            include_deprecated=config.include_deprecated
        )

        # 解析 OpenAPI
        parse_result: OpenAPIParseResult = import_openapi(source, filter_config=filter_config)

        # 按 tags 分组
        modules_dict: Dict[str, List[OpenAPIRequestModel]] = {}
        for req in parse_result.requests:
            # 取第一个 tag 作为模块名，没有则归入"未分类"
            module_name = req.tags[0] if req.tags else "未分类"
            if module_name not in modules_dict:
                modules_dict[module_name] = []
            modules_dict[module_name].append(req)

        # 构建预览树
        rows = []
        total_apis = 0

        for module_name, apis in modules_dict.items():
            test_cases = []
            for api in apis:
                api_item = PreviewApiItem(
                    name=api.name or api.operation_id or f"{api.method.value} {api.path}",
                    method=api.method.value,
                    path=api.path,
                    status=ItemStatus.NEW,
                    request_type=api.request_type,
                    json_data=api.json_data,
                    headers=[{"key": h.key, "value": h.value} for h in api.headers_list] if config.import_headers else [],
                    params=[{"key": p.key, "value": p.value} for p in api.params_list] if config.import_params else [],
                    cookies=[{"key": c.key, "value": c.value} for c in api.cookies_list] if config.import_cookies else [],
                    formdata=[{"key": f.key, "value": f.value} for f in api.formdata] if config.import_body else [],
                    description=api.description
                )
                test_cases.append(api_item)
                total_apis += 1

            module_item = PreviewModuleItem(
                name=module_name,
                status=ItemStatus.NEW,
                test_cases=test_cases,
                count=len(test_cases)
            )
            rows.append(module_item)

        # 构建预览信息
        info = PreviewInfo(
            title=parse_result.info.title,
            version=parse_result.info.version,
            openapi_version=parse_result.info.openapi_version,
            description=parse_result.info.description,
            total_modules=len(rows),
            total_apis=total_apis,
            new_modules=len(rows),
            new_apis=total_apis
        )

        return PreviewResult(
            code=200,
            msg="解析成功",
            success=True,
            time=datetime.now(),
            data={
                "info": info.model_dump(by_alias=True),
                "rows": [r.model_dump(by_alias=True) for r in rows]
            }
        )

    except Exception as e:
        return PreviewResult(
            code=500,
            msg=f"解析失败: {str(e)}",
            success=False,
            time=datetime.now(),
            data={}
        )


async def analyze_diff(
    preview: PreviewResult,
    db: AsyncSession,
    config: ImportConfig
) -> PreviewResult:
    """
    与数据库现有数据对比分析

    Args:
        preview: 预览结果
        db: 数据库会话
        config: 导入配置

    Returns:
        PreviewResult: 更新后的预览结果（包含匹配信息）
    """
    if not preview.success:
        return preview

    try:
        rows = preview.data.get("rows", [])
        info = preview.data.get("info", {})

        # 查询目标范围内的现有模块
        if config.target_module_id:
            # 指定了目标模块，查询该模块下的子模块
            stmt = select(ApiProjectSubmodules).where(
                and_(
                    ApiProjectSubmodules.project_id == config.project_id,
                    ApiProjectSubmodules.parent_id == config.target_module_id,
                    ApiProjectSubmodules.del_flag == "0",
                    ApiProjectSubmodules.type == "1"  # 接口模块类型
                )
            )
        else:
            # 未指定目标模块，查询一级模块（parent_id 为 None）
            stmt = select(ApiProjectSubmodules).where(
                and_(
                    ApiProjectSubmodules.project_id == config.project_id,
                    ApiProjectSubmodules.parent_id.is_(None),
                    ApiProjectSubmodules.del_flag == "0",
                    ApiProjectSubmodules.type == "1"
                )
            )

        result = await db.execute(stmt)
        existing_modules = {m.name: m for m in result.scalars().all()}

        new_modules_count = 0
        new_apis_count = 0
        update_apis_count = 0

        # 遍历预览数据进行对比
        for module_data in rows:
            module_name = module_data.get("name")

            # 模块匹配
            if config.module_strategy == ModuleStrategy.AUTO_MATCH:
                if module_name in existing_modules:
                    matched_module = existing_modules[module_name]
                    module_data["status"] = ItemStatus.MATCH.value
                    module_data["matchedModuleId"] = matched_module.id
                    module_data["moduleId"] = matched_module.id
                else:
                    module_data["status"] = ItemStatus.NEW.value
                    new_modules_count += 1
            elif config.module_strategy == ModuleStrategy.CREATE_ALL:
                module_data["status"] = ItemStatus.NEW.value
                new_modules_count += 1
            elif config.module_strategy == ModuleStrategy.TARGET_ONLY:
                # 只导入到目标模块，不创建新模块
                if config.target_module_id:
                    module_data["status"] = ItemStatus.MATCH.value
                    module_data["matchedModuleId"] = config.target_module_id
                    module_data["moduleId"] = config.target_module_id
                else:
                    module_data["status"] = ItemStatus.NEW.value
                    new_modules_count += 1

            # 获取该模块下的现有接口（用于对比）
            matched_module_id = module_data.get("matchedModuleId")
            existing_apis = {}

            if matched_module_id:
                api_stmt = select(ApiTestCases).where(
                    and_(
                        ApiTestCases.parent_submodule_id == matched_module_id,
                        ApiTestCases.case_type == "1",
                        ApiTestCases.del_flag == "0"
                    )
                )
                api_result = await db.execute(api_stmt)
                for api in api_result.scalars().all():
                    # 使用 (名称, 方法) 作为匹配键
                    key = f"{api.name}::{api.method.value if api.method else ''}"
                    existing_apis[key] = api

            # 接口匹配
            test_cases = module_data.get("testCases", [])
            for api_data in test_cases:
                api_name = api_data.get("name")
                api_method = api_data.get("method")
                match_key = f"{api_name}::{api_method}"

                if match_key in existing_apis:
                    matched_api = existing_apis[match_key]
                    api_data["status"] = ItemStatus.MATCH.value
                    api_data["matchedCaseId"] = matched_api.case_id
                    api_data["caseId"] = matched_api.case_id

                    # 检测变更字段
                    changes = []
                    if api_data.get("path") != matched_api.path:
                        changes.append("path")
                    if api_data.get("requestType") != (matched_api.request_type.value if matched_api.request_type else None):
                        changes.append("requestType")
                    if api_data.get("jsonData") != matched_api.json_data:
                        changes.append("jsonData")
                    api_data["changes"] = changes
                    update_apis_count += 1
                else:
                    api_data["status"] = ItemStatus.NEW.value
                    new_apis_count += 1

        # 更新统计信息
        info["newModules"] = new_modules_count
        info["newApis"] = new_apis_count
        info["updateApis"] = update_apis_count

        return PreviewResult(
            code=200,
            msg="对比分析完成",
            success=True,
            time=datetime.now(),
            data={
                "info": info,
                "rows": rows
            }
        )

    except Exception as e:
        return PreviewResult(
            code=500,
            msg=f"对比分析失败: {str(e)}",
            success=False,
            time=datetime.now(),
            data=preview.data
        )


async def execute_import(
    preview: PreviewResult,
    db: AsyncSession,
    config: ImportExecuteConfig
) -> ImportResult:
    """
    执行导入操作

    Args:
        preview: 预览结果（经过 analyze_diff 处理）
        db: 数据库会话
        config: 执行配置（包含用户选择）

    Returns:
        ImportResult: 导入结果
    """
    if not preview.success:
        return ImportResult(
            code=500,
            msg=preview.msg,
            success=False,
            data=ImportResultDetail(errors=[preview.msg])
        )

    result_detail = ImportResultDetail()

    try:
        rows = preview.data.get("rows", [])

        for module_data in rows:
            module_name = module_data.get("name")

            # 检查是否被用户选中
            if config.selected_modules is not None:
                if module_name not in config.selected_modules:
                    continue

            module_id = module_data.get("matchedModuleId")
            module_status = module_data.get("status")

            # 处理模块
            if module_status == ItemStatus.NEW.value:
                # 创建新模块
                new_module = ApiProjectSubmodules(
                    name=module_name,
                    type="1",  # 接口模块类型
                    parent_id=config.target_module_id,
                    project_id=config.project_id
                )
                db.add(new_module)
                await db.flush()
                module_id = new_module.id
                result_detail.modules_created += 1

            # 处理该模块下的接口
            test_cases = module_data.get("testCases", [])
            for api_data in test_cases:
                api_name = api_data.get("name")
                api_method = api_data.get("method")
                api_status = api_data.get("status")
                matched_case_id = api_data.get("matchedCaseId")

                # 检查是否被用户选中
                if config.selected_apis is not None:
                    api_key = f"{module_name}::{api_name}::{api_method}"
                    if api_key not in config.selected_apis:
                        continue

                if api_status == ItemStatus.NEW.value:
                    # 新增接口
                    await _create_api(db, api_data, module_id, config)
                    result_detail.apis_created += 1

                elif api_status == ItemStatus.MATCH.value:
                    # 已存在的接口
                    if config.conflict_strategy == ConflictStrategy.SKIP:
                        result_detail.apis_skipped += 1

                    elif config.conflict_strategy == ConflictStrategy.OVERWRITE:
                        # 覆盖：删除原有数据后新增
                        await _delete_api_related_data(db, matched_case_id)
                        await _update_api(db, api_data, matched_case_id, config, overwrite=True)
                        result_detail.apis_updated += 1

                    elif config.conflict_strategy == ConflictStrategy.SMART_MERGE:
                        # 智能合并：保留断言、前置、后置
                        await _update_api(db, api_data, matched_case_id, config, overwrite=False)
                        result_detail.apis_updated += 1

        await db.commit()

        return ImportResult(
            code=200,
            msg="导入成功",
            success=True,
            time=datetime.now(),
            data=result_detail
        )

    except Exception as e:
        await db.rollback()
        result_detail.errors.append(str(e))
        return ImportResult(
            code=500,
            msg=f"导入失败: {str(e)}",
            success=False,
            time=datetime.now(),
            data=result_detail
        )


# ==================== 辅助函数 ====================

async def _create_api(
    db: AsyncSession,
    api_data: Dict,
    module_id: int,
    config: ImportExecuteConfig
) -> int:
    """创建新接口"""
    # 创建测试用例
    new_case = ApiTestCases(
        name=api_data.get("name"),
        case_type="1",
        parent_submodule_id=module_id,
        project_id=config.project_id,
        path=api_data.get("path"),
        method=Request_method(api_data.get("method")),
        request_type=Request_Type(api_data.get("requestType")) if api_data.get("requestType") else Request_Type.NONE,
        json_data=api_data.get("jsonData") if config.import_body else None,
        is_run=1,
        status_code=200
    )
    db.add(new_case)
    await db.flush()
    case_id = new_case.case_id

    # 创建 headers
    if config.import_headers:
        for header in api_data.get("headers", []):
            db.add(ApiHeaders(
                case_id=case_id,
                key=header.get("key"),
                value=header.get("value", "")
            ))

    # 创建 params
    if config.import_params:
        for param in api_data.get("params", []):
            db.add(ApiParams(
                case_id=case_id,
                key=param.get("key"),
                value=param.get("value", "")
            ))

    # 创建 cookies
    if config.import_cookies:
        for cookie in api_data.get("cookies", []):
            db.add(ApiCookies(
                case_id=case_id,
                key=cookie.get("key"),
                value=cookie.get("value", "")
            ))

    # 创建 formdata
    if config.import_body:
        for formdata in api_data.get("formdata", []):
            db.add(ApiFormdata(
                case_id=case_id,
                key=formdata.get("key"),
                value=formdata.get("value", "")
            ))

    await db.flush()
    return case_id


async def _update_api(
    db: AsyncSession,
    api_data: Dict,
    case_id: int,
    config: ImportExecuteConfig,
    overwrite: bool = False
) -> None:
    """更新接口"""
    # 获取现有用例
    stmt = select(ApiTestCases).where(ApiTestCases.case_id == case_id)
    result = await db.execute(stmt)
    existing_case = result.scalars().first()

    if not existing_case:
        return

    # 更新基本信息
    existing_case.path = api_data.get("path") or existing_case.path
    if api_data.get("requestType"):
        existing_case.request_type = Request_Type(api_data.get("requestType"))

    if config.import_body and api_data.get("jsonData") is not None:
        if overwrite:
            existing_case.json_data = api_data.get("jsonData")
        else:
            # 智能合并：如果是字典则深度合并
            if isinstance(existing_case.json_data, dict) and isinstance(api_data.get("jsonData"), dict):
                merged = {**existing_case.json_data, **api_data.get("jsonData")}
                existing_case.json_data = merged
            else:
                existing_case.json_data = api_data.get("jsonData")

    if overwrite:
        # 覆盖模式：删除并重新创建 headers, params, cookies, formdata
        # 注意：断言、前置、后置在 _delete_api_related_data 中已删除

        # 删除现有的
        await db.execute(delete(ApiHeaders).where(ApiHeaders.case_id == case_id))
        await db.execute(delete(ApiParams).where(ApiParams.case_id == case_id))
        await db.execute(delete(ApiCookies).where(ApiCookies.case_id == case_id))
        await db.execute(delete(ApiFormdata).where(ApiFormdata.case_id == case_id))

        # 重新创建
        if config.import_headers:
            for header in api_data.get("headers", []):
                db.add(ApiHeaders(case_id=case_id, key=header.get("key"), value=header.get("value", "")))

        if config.import_params:
            for param in api_data.get("params", []):
                db.add(ApiParams(case_id=case_id, key=param.get("key"), value=param.get("value", "")))

        if config.import_cookies:
            for cookie in api_data.get("cookies", []):
                db.add(ApiCookies(case_id=case_id, key=cookie.get("key"), value=cookie.get("value", "")))

        if config.import_body:
            for formdata in api_data.get("formdata", []):
                db.add(ApiFormdata(case_id=case_id, key=formdata.get("key"), value=formdata.get("value", "")))

    else:
        # 智能合并模式：只添加新的，不删除现有的
        if config.import_headers:
            existing_headers = set()
            stmt = select(ApiHeaders).where(ApiHeaders.case_id == case_id)
            result = await db.execute(stmt)
            for h in result.scalars().all():
                existing_headers.add(h.key)

            for header in api_data.get("headers", []):
                if header.get("key") not in existing_headers:
                    db.add(ApiHeaders(case_id=case_id, key=header.get("key"), value=header.get("value", "")))

        if config.import_params:
            existing_params = set()
            stmt = select(ApiParams).where(ApiParams.case_id == case_id)
            result = await db.execute(stmt)
            for p in result.scalars().all():
                existing_params.add(p.key)

            for param in api_data.get("params", []):
                if param.get("key") not in existing_params:
                    db.add(ApiParams(case_id=case_id, key=param.get("key"), value=param.get("value", "")))

        if config.import_cookies:
            existing_cookies = set()
            stmt = select(ApiCookies).where(ApiCookies.case_id == case_id)
            result = await db.execute(stmt)
            for c in result.scalars().all():
                existing_cookies.add(c.key)

            for cookie in api_data.get("cookies", []):
                if cookie.get("key") not in existing_cookies:
                    db.add(ApiCookies(case_id=case_id, key=cookie.get("key"), value=cookie.get("value", "")))

        if config.import_body:
            existing_formdata = set()
            stmt = select(ApiFormdata).where(ApiFormdata.case_id == case_id)
            result = await db.execute(stmt)
            for f in result.scalars().all():
                existing_formdata.add(f.key)

            for formdata in api_data.get("formdata", []):
                if formdata.get("key") not in existing_formdata:
                    db.add(ApiFormdata(case_id=case_id, key=formdata.get("key"), value=formdata.get("value", "")))

    await db.flush()


async def _delete_api_related_data(db: AsyncSession, case_id: int) -> None:
    """删除接口相关数据（覆盖模式使用）"""
    # 删除断言
    await db.execute(delete(ApiAssertions).where(ApiAssertions.case_id == case_id))
    # 删除前置
    await db.execute(delete(ApiSetup).where(ApiSetup.case_id == case_id))
    # 删除后置
    await db.execute(delete(ApiTeardown).where(ApiTeardown.case_id == case_id))
    # 删除 headers
    await db.execute(delete(ApiHeaders).where(ApiHeaders.case_id == case_id))
    # 删除 params
    await db.execute(delete(ApiParams).where(ApiParams.case_id == case_id))
    # 删除 cookies
    await db.execute(delete(ApiCookies).where(ApiCookies.case_id == case_id))
    # 删除 formdata
    await db.execute(delete(ApiFormdata).where(ApiFormdata.case_id == case_id))

    await db.flush()


# ==================== 便捷函数 ====================

async def import_openapi_to_db(
    source: str,
    db: AsyncSession,
    config: ImportExecuteConfig
) -> ImportResult:
    """
    一键导入 OpenAPI 到数据库（便捷函数）

    Args:
        source: OpenAPI 规范的 URL 或文件路径
        db: 数据库会话
        config: 导入配置

    Returns:
        ImportResult: 导入结果
    """
    # Step 1: 解析为预览
    preview = parse_to_preview(source, config)
    if not preview.success:
        return ImportResult(
            code=500,
            msg=preview.msg,
            success=False,
            data=ImportResultDetail(errors=[preview.msg])
        )

    # Step 2: 对比分析
    preview = await analyze_diff(preview, db, config)
    if not preview.success:
        return ImportResult(
            code=500,
            msg=preview.msg,
            success=False,
            data=ImportResultDetail(errors=[preview.msg])
        )

    # Step 3: 执行导入
    return await execute_import(preview, db, config)


# ==================== 测试入口 ====================

if __name__ == '__main__':
    import json

    # 测试解析预览
    print("=" * 60)
    print("测试解析预览功能")
    print("=" * 60)

    config = ImportConfig(
        project_id=1,
        target_module_id=None,
        module_strategy=ModuleStrategy.AUTO_MATCH,
        conflict_strategy=ConflictStrategy.SMART_MERGE
    )

    # 使用本地文件测试
    preview = parse_to_preview(
        r'D:\code\project\fast_api_admin\utils\api_import\openapi.json',
        config
    )

    if preview.success:
        info = preview.data.get("info", {})
        rows = preview.data.get("rows", [])

        print(f"\nAPI 标题: {info.get('title')}")
        print(f"API 版本: {info.get('version')}")
        print(f"总模块数: {info.get('totalModules')}")
        print(f"总接口数: {info.get('totalApis')}")

        print(f"\n前3个模块预览:")
        for i, module in enumerate(rows[:3], 1):
            print(f"\n--- 模块 {i}: {module.get('name')} ---")
            print(f"  状态: {module.get('status')}")
            print(f"  接口数: {module.get('count')}")
            for api in module.get("testCases", [])[:3]:
                print(f"    • {api.get('method')} {api.get('name')}")
    else:
        print(f"解析失败: {preview.msg}")

    # 输出完整的预览 JSON（与 demo.md 格式对比）
    print("\n" + "=" * 60)
    print("预览数据结构示例（前2个模块）")
    print("=" * 60)

    if preview.success and rows:
        sample_data = {
            "code": preview.code,
            "msg": preview.msg,
            "data": {
                "info": info,
                "rows": rows[:2]
            },
            "success": preview.success
        }
        print(json.dumps(sample_data, ensure_ascii=False, indent=2, default=str)[:2000])
