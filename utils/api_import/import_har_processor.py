#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : fast_api_admin
@File    : import_har_processor.py
@Author  : Claude
@Date    : 2025-12-06
@Description : HAR 文件导入处理器
支持解析、预览、导入完整流程（与 OpenAPI 导入逻辑一致）
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncSession

from config.enums import Request_method, Request_Type
from module_admin.api_project_submodules.entity.do.project_submodules_do import ApiProjectSubmodules
from module_admin.api_testing.api_test_cases.entity.do.test_cases_do import ApiTestCases
from module_admin.api_testing.api_headers.entity.do.headers_do import ApiHeaders
from module_admin.api_testing.api_params.entity.do.params_do import ApiParams
from module_admin.api_testing.api_cookies.entity.do.cookies_do import ApiCookies
from module_admin.api_testing.api_formdata.entity.do.formdata_do import ApiFormdata

from utils.api_import.import_har import (
    parse_har_to_requests,
    HarRequestModel,
    HarFilterConfig
)


# ==================== 配置模型 ====================

class HarImportConfig(BaseModel):
    """HAR 导入配置"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # 目标配置
    project_id: int = Field(description='目标项目ID')
    target_module_id: Optional[int] = Field(default=None, description='目标模块ID，None表示创建新模块')
    module_name: Optional[str] = Field(default=None, description='新模块名称（当 target_module_id 为空时使用）')

    # 导入选项
    import_headers: bool = Field(default=True, description='是否导入headers')
    import_params: bool = Field(default=True, description='是否导入params')
    import_body: bool = Field(default=True, description='是否导入请求体')
    import_cookies: bool = Field(default=True, description='是否导入cookies')

    # HAR 过滤配置
    filter_static: bool = Field(default=True, description='是否过滤静态资源')
    allowed_methods: Optional[List[str]] = Field(default=None, description='允许的HTTP方法')
    include_domains: Optional[List[str]] = Field(default=None, description='只包含的域名')
    url_keywords: Optional[List[str]] = Field(default=None, description='URL关键词过滤')


class HarImportExecuteConfig(HarImportConfig):
    """执行导入的配置（包含用户选择）"""
    selected_apis: Optional[List[str]] = Field(
        default=None,
        description='选中的接口标识列表（格式: name::method），None表示全选'
    )


# ==================== 预览数据模型 ====================

class HarPreviewApiItem(BaseModel):
    """预览接口项"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(description='唯一标识（用于前端 tree 的 key）')
    name: str = Field(description='接口名称')
    method: str = Field(description='请求方法')
    path: str = Field(description='请求路径')
    type: str = Field(default="api", description='类型')
    status: str = Field(default="new", description='状态: new')
    domain: Optional[str] = Field(default=None, description='域名')

    # 原始数据（用于导入）
    request_type: Optional[str] = Field(default=None)
    json_data: Optional[Any] = Field(default=None)
    headers: List[Dict] = Field(default=[])
    params: List[Dict] = Field(default=[])
    cookies: List[Dict] = Field(default=[])
    formdata: List[Dict] = Field(default=[])


class HarPreviewInfo(BaseModel):
    """预览信息"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    file_name: str = Field(description='文件名')
    total_apis: int = Field(description='接口总数')
    domains: List[str] = Field(default=[], description='包含的域名列表')
    methods: Dict[str, int] = Field(default={}, description='方法统计')


class HarPreviewResult(BaseModel):
    """预览结果"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    code: int = Field(default=200)
    msg: str = Field(default="解析成功")
    success: bool = Field(default=True)
    time: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any] = Field(default={})


# ==================== 导入结果模型 ====================

class HarImportResultDetail(BaseModel):
    """导入结果详情"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    module_created: bool = Field(default=False, description='是否创建了新模块')
    module_id: Optional[int] = Field(default=None, description='模块ID')
    module_name: Optional[str] = Field(default=None, description='模块名称')
    apis_created: int = Field(default=0, description='创建的接口数')
    errors: List[str] = Field(default=[], description='错误信息列表')


class HarImportResult(BaseModel):
    """导入结果"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    code: int = Field(default=200)
    msg: str = Field(default="导入成功")
    success: bool = Field(default=True)
    time: datetime = Field(default_factory=datetime.now)
    data: HarImportResultDetail = Field(default_factory=HarImportResultDetail)


# ==================== 核心函数 ====================

def har_parse_to_preview(
    file_path: str,
    file_name: str,
    config: HarImportConfig
) -> HarPreviewResult:
    """
    解析 HAR 文件为预览结构（不涉及数据库）

    Args:
        file_path: HAR 文件路径
        file_name: 原始文件名
        config: 导入配置

    Returns:
        HarPreviewResult: 预览结果
    """
    try:
        # 构建过滤配置
        filter_config = HarFilterConfig(
            filter_static=config.filter_static,
            allowed_methods=config.allowed_methods,
            include_domains=config.include_domains,
            url_keywords=config.url_keywords
        )

        # 解析 HAR 文件
        har_requests: List[HarRequestModel] = parse_har_to_requests(file_path, filter_config)

        # 构建预览数据
        rows = []
        domains = set()
        methods_count = {}

        for idx, req in enumerate(har_requests):
            # 提取域名
            parsed_url = urlparse(req.path)
            domain = parsed_url.netloc
            if domain:
                domains.add(domain)

            # 方法统计
            method = req.method.value
            methods_count[method] = methods_count.get(method, 0) + 1

            # 构建预览项
            api_item = HarPreviewApiItem(
                id=f"api_{idx}",
                name=req.name,
                method=method,
                path=req.path,
                status="new",
                domain=domain,
                request_type=req.request_type.value if req.request_type else None,
                json_data=req.json_data if config.import_body else None,
                headers=[{"key": h.key, "value": h.value} for h in req.headers_list] if config.import_headers else [],
                params=[{"key": p.key, "value": p.value} for p in req.params_list] if config.import_params else [],
                cookies=[{"key": c.key, "value": c.value} for c in req.cookies_list] if config.import_cookies else [],
                formdata=[{"key": f.key, "value": f.value} for f in req.formdata] if config.import_body else []
            )
            rows.append(api_item)

        # 构建预览信息
        info = HarPreviewInfo(
            file_name=file_name,
            total_apis=len(rows),
            domains=list(domains),
            methods=methods_count
        )

        return HarPreviewResult(
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
        return HarPreviewResult(
            code=500,
            msg=f"解析失败: {str(e)}",
            success=False,
            time=datetime.now(),
            data={}
        )


async def har_execute_import(
    preview: HarPreviewResult,
    db: AsyncSession,
    config: HarImportExecuteConfig
) -> HarImportResult:
    """
    执行 HAR 导入操作

    Args:
        preview: 预览结果
        db: 数据库会话
        config: 执行配置（包含用户选择）

    Returns:
        HarImportResult: 导入结果
    """
    if not preview.success:
        return HarImportResult(
            code=500,
            msg=preview.msg,
            success=False,
            data=HarImportResultDetail(errors=[preview.msg])
        )

    result_detail = HarImportResultDetail()

    try:
        rows = preview.data.get("rows", [])
        module_id = config.target_module_id
        module_name = config.module_name

        # 如果没有指定目标模块，则创建新模块
        if not module_id:
            # 使用传入的模块名或默认名称
            if not module_name:
                module_name = f"HAR导入_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            new_module = ApiProjectSubmodules(
                name=module_name,
                type="1",  # 接口模块类型
                parent_id=None,  # 一级模块
                project_id=config.project_id
            )
            db.add(new_module)
            await db.flush()
            module_id = new_module.id
            result_detail.module_created = True

        result_detail.module_id = module_id
        result_detail.module_name = module_name

        # 导入接口
        for api_data in rows:
            api_name = api_data.get("name")
            api_method = api_data.get("method")

            # 检查是否被用户选中
            if config.selected_apis is not None:
                api_key = f"{api_name}::{api_method}"
                if api_key not in config.selected_apis:
                    continue

            # 创建新接口
            await _create_har_api(db, api_data, module_id, config)
            result_detail.apis_created += 1

        await db.commit()

        return HarImportResult(
            code=200,
            msg=f"导入成功：新增 {result_detail.apis_created} 个接口",
            success=True,
            time=datetime.now(),
            data=result_detail
        )

    except Exception as e:
        await db.rollback()
        result_detail.errors.append(str(e))
        return HarImportResult(
            code=500,
            msg=f"导入失败: {str(e)}",
            success=False,
            time=datetime.now(),
            data=result_detail
        )


# ==================== 辅助函数 ====================

async def _create_har_api(
    db: AsyncSession,
    api_data: Dict,
    module_id: int,
    config: HarImportExecuteConfig
) -> int:
    """创建新接口"""
    # 创建测试用例
    request_type_value = api_data.get("requestType")
    new_case = ApiTestCases(
        name=api_data.get("name"),
        case_type="1",
        parent_submodule_id=module_id,
        project_id=config.project_id,
        path=api_data.get("path"),
        method=Request_method(api_data.get("method")),
        request_type=Request_Type(request_type_value) if request_type_value else Request_Type.NONE,
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


# ==================== 测试入口 ====================

if __name__ == '__main__':
    import json

    # 测试解析预览
    print("=" * 60)
    print("测试 HAR 解析预览功能")
    print("=" * 60)

    config = HarImportConfig(
        project_id=1,
        target_module_id=None,
        filter_static=True
    )

    # 使用本地文件测试（需要有测试文件）
    test_file = r'D:\code\project\fast_api_admin\CaseGo\upload_path\files\2025\11\17\file_20251117181517_380fc2f1_291973.har'

    try:
        preview = har_parse_to_preview(test_file, "test.har", config)

        if preview.success:
            info = preview.data.get("info", {})
            rows = preview.data.get("rows", [])

            print(f"\n文件名: {info.get('fileName')}")
            print(f"接口总数: {info.get('totalApis')}")
            print(f"域名列表: {info.get('domains')}")
            print(f"方法统计: {info.get('methods')}")

            print(f"\n前5个接口预览:")
            for i, api in enumerate(rows[:5], 1):
                print(f"  {i}. [{api.get('method')}] {api.get('name')}")
                print(f"     Path: {api.get('path')[:80]}...")
        else:
            print(f"解析失败: {preview.msg}")

    except FileNotFoundError:
        print("测试文件不存在，跳过测试")
