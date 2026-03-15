from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, Any, List, Dict, Union, ClassVar

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from config.enums import Request_Type, Request_method
from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_testing.api_assertions.entity.vo.assertions_vo import AssertionsPageQueryModel, AssertionsModel
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesPageQueryModel, CookiesModel
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataPageQueryModel, FormdataModel, \
    FileConfig
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersPageQueryModel, HeadersModel
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsPageQueryModel, ParamsModel
from module_admin.api_testing.api_setup.entity.vo.setup_vo import SetupPageQueryModel, SetupModel
from module_admin.api_testing.api_teardown.entity.vo.teardown_vo import TeardownPageQueryModel, TeardownModel


class Test_casesModel(BaseModel):
    """
    接口用例表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    case_id: Optional[int] = Field(default=None, description='测试用例ID')
    name: Optional[str] = Field(default=None, description='测试用例名称')
    case_type: Optional[str] = Field(default=None, description='测试用例类型 (1接口, 2用例等)')
    copy_id: Optional[int] = Field(default=None, description='复制过来的接口用例ID')
    parent_case_id: Optional[int] = Field(default=None, description='父级测试接口ID')
    parent_submodule_id: Optional[int] = Field(default=None, description='父级模块ID')
    project_id: Optional[int] = Field(default=None, description='所属项目id')
    description: Optional[str] = Field(default=None, description='测试接口/用例描述')
    path: Optional[str] = Field(default=None, description='请求路径')
    method: Optional[Request_method] = Field(default=Request_method.GET, description='请求方法 (GET, POST等)')
    request_type: Optional[Request_Type] = Field(default=Request_Type.NONE,
                                                 description='请求类型 (1-None,2-Form Data,3-x-www-form-urlencoded,4-JSON, 5-xml,6-Raw,7-Binary,8-File)')
    is_run: Optional[int] = Field(default=None, description='是否执行')
    status_code: Optional[int] = Field(default=None, description='预期状态码')
    sleep: Optional[int] = Field(default=None, description='执行前等待时间 (毫秒)')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    json_data: Optional[dict | List[dict] | str] = Field(default={}, description='请求数据')
    case_file_config: Optional[FileConfig | dict] = Field(default=None, description='用例的文件配置')
    response_example: Optional[dict | List[dict] | str] = Field(default=None, description='返回示例')

    # from_data: Optional[str] = Field(default=None, description='请求数据')
    # file_path: Optional[str] = Field(default=None, description='文件路径(用于文件上传)')

    def validate_fields(self):
        pass


# class Test_cases_all_Model(Test_casesModel):
#     api_teardown = True


class Test_casesQueryModel(Test_casesModel):
    """
    接口用例不分页查询模型
    """
    pass


class Test_casesImportModel(Test_casesModel):
    """
    接口用例导入模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    url: Optional[str] = Field(default=None, description='url')
    target_module_id: Optional[int | str] = Field(default=None, description='目标模块ID'),
    project_id: Optional[int | str] = Field(default=None, description='项目id'),




@as_query
class Test_casesPageQueryModel(Test_casesQueryModel):
    """
    接口用例分页查询模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTest_casesModel(BaseModel):
    """
    删除接口用例模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    case_ids: str = Field(description='需要删除的测试用例ID')


class Test_casesAllParamsQueryModel(Test_casesModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    cookies_list: Optional[List[CookiesModel]] = Field(default=[])
    headers_list: Optional[List[HeadersModel]] = Field(default=[])
    params_list: Optional[List[ParamsModel]] = Field(default=[])
    setup_list: Optional[List[SetupModel]] = Field(default=[])
    teardown_list: Optional[List[TeardownModel]] = Field(default=[])
    assertion_list: Optional[List[AssertionsModel]] = Field(default=[])
    formdata: Optional[List[FormdataModel]] = Field(default=[])


class Test_casesExecModel(Test_casesModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    env_id: int = Field(default=1, description='执行环境')
    use_env_cookies: bool = Field(default=False, description='是否使用环境级别的Cookies（请求前加载、请求后存储）')


class APIResponse(BaseModel):
    """API响应模型"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True
    )

    case_id: Optional[int] = Field(default=None, description='用例ID')
    case_name: Optional[str] = Field(default=None, description='用例名称')
    env_id: Optional[int] = Field(default=None, description='环境ID')
    request_url: Optional[str] = Field(default=None, description='请求URL')
    request_method: Optional[str] = Field(default=None, description='请求方法')
    request_headers: Optional[Dict[str, Any]] = Field(default=None, description='请求头')
    request_params: Optional[Dict[str, Any]] = Field(default=None, description='请求参数')
    request_body: Optional[Any] = Field(default=None, description='请求体')
    request_cookies: Optional[Dict[str, Any]] = Field(default=None, description='请求Cookies')
    response_cookies: Optional[Dict[str, Any]] = Field(default=None, description='响应Cookies')
    response_status_code: int = Field(description='响应状态码')
    response_headers: Optional[Dict[str, Any]] = Field(default=None, description='响应头')
    response_body: Optional[Union[str, Dict[str, Any]]] = Field(default=None, description='响应体')
    response_time: Optional[float] = Field(default=None, description='响应时间（秒）')
    execution_time: Optional[datetime] = Field(default=None, description='执行时间')
    is_success: bool = Field(description='是否成功')
    error_message: Optional[str] = Field(default=None, description='错误信息')
    # setup_results: Optional[Dict[str, Any]] = Field(default=None, description='前置操作结果')
    # teardown_results: Optional[Dict[str, Any]] = Field(default=None, description='后置操作结果')
    # assertion_results: Optional[Dict[str, Any]] = Field(default=None, description='断言结果')


class ApiExecutorParameters(BaseModel):
    """
    执行器入参（支持数据库连接与序列化分离）
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

    case_id: int = Field(description='用例ID')
    env_id: int = Field(description='执行环境ID')
    user_id: int = Field(description='用户ID')


class Input_Parameters(BaseModel):
    """
    执行器入参（支持数据库连接与序列化分离）
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

    case_id: int = Field(description='用例ID')
    description: Optional[str] = Field(description='用户的需求描述')


class Test_cases_generator(Test_casesModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    inputs: Optional[Input_Parameters] = Field(description='执行环境')
    response_mode: Optional[str] = Field(default="streaming")
    user: Optional[str] = Field(default="")


class Test_case_sort(Test_casesModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    pass
