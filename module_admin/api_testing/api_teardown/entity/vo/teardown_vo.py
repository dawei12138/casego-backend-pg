from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional, List, Dict
from module_admin.annotation.pydantic_annotation import as_query


class TeardownModel(BaseModel):
    """
    接口后置操作表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    teardown_id: Optional[int] = Field(default=None, description='操作ID')
    name: Optional[str] = Field(default=None, description='操作名称')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    teardown_type: Optional[str] = Field(default=None,
                                         description='操作类型 (extract_variable, db_operation, custom_script, wait_time)')
    extract_variable_method: Optional[str] = Field(default=None,
                                                   description='提取响应的方法： response_textresponse_jsonresponse_xmlresponse_headerresponse_cookie')
    jsonpath: Optional[str] = Field(default=None, description='jsonpath提取表达式（用于提取变量）')
    extract_index: Optional[int] = Field(default=None, description='提取索引')
    extract_index_is_run: Optional[int] = Field(default=None, description='是否执行提取索引操作')
    variable_name: Optional[str] = Field(default=None, description='变量名称（用于存储提取的数据）')
    extract_variables: Optional[List[Dict[str, Optional[str]]]] = Field(
        default=[{"variable_name": None, "jsonpath": None}],
        description='提取额外参数的KEY-VALUE')
    regular_expression: Optional[str] = Field(default=None, description='正则提取表达式（用于提取变量）')
    xpath_expression: Optional[str] = Field(default=None, description='xpath提取表达式（用于提取变量）')
    response_header: Optional[str] = Field(default=None, description='header提取表达式（用于提取变量）')
    response_cookie: Optional[str] = Field(default=None, description='cookie提取表达式（用于提取变量）')

    database_id: Optional[int] = Field(default=None, description='数据库连接ID')
    db_operation: Optional[str] = Field(default=None, description='数据库操作语句（用于数据库操作）')
    script: Optional[str] = Field(default=None, description='自定义脚本语句（用于自定义脚本）')
    wait_time: Optional[int] = Field(default=None, description='等待时间（毫秒，用于等待时间）')
    is_run: Optional[int] = Field(default=None, description='是否执行该后置操作')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='case_id', message='关联的测试用例ID不能为空')
    def get_case_id(self):
        return self.case_id

    @NotBlank(field_name='teardown_type',
              message='操作类型 (extract_variable, db_operation, custom_script, wait_time)不能为空')
    def get_teardown_type(self):
        return self.teardown_type

    def validate_fields(self):
        self.get_case_id()
        self.get_teardown_type()


class TeardownQueryModel(TeardownModel):
    """
    接口后置操作不分页查询模型
    """
    pass


@as_query
class TeardownPageQueryModel(TeardownQueryModel):
    """
    接口后置操作分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTeardownModel(BaseModel):
    """
    删除接口后置操作模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    teardown_ids: str = Field(description='需要删除的操作ID')
