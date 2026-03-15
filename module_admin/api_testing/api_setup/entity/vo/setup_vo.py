from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional, List, Dict
from module_admin.annotation.pydantic_annotation import as_query


class SetupModel(BaseModel):
    """
    接口前置操作表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    setup_id: Optional[int] = Field(default=None, description='操作ID')
    name: Optional[str] = Field(default=None, description='操作名称')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    setup_type: Optional[str] = Field(default=None, description='操作类型 (db_connection, execute_script, wait_time)')
    db_connection_id: Optional[int] = Field(default=None, description='数据库连接ID')
    script: Optional[str] = Field(default=None, description='脚本语句')
    extract_variables: Optional[List[Dict[str, Optional[str]]]] = Field(default=[{"variable_name": None, "jsonpath": None}], description='提取额外参数的KEY-VALUE')
    jsonpath: Optional[str] = Field(default=None, description='jsonpath提取表达式')
    variable_name: Optional[str] = Field(default=None, description='变量名称（用于存储提取的数据）')
    wait_time: Optional[int] = Field(default=None, description='等待时间（毫秒）')
    extract_index: Optional[int] = Field(default=None, description='提取索引')
    extract_index_is_run: Optional[int] = Field(default=None, description='是否执行提取索引操作')
    is_run: Optional[int] = Field(default=None, description='是否执行该前置操作')
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

    @NotBlank(field_name='setup_type', message='操作类型 (db_connection, execute_script, wait_time)不能为空')
    def get_setup_type(self):
        return self.setup_type

    def validate_fields(self):
        self.get_case_id()
        self.get_setup_type()


class SetupQueryModel(SetupModel):
    """
    接口前置操作不分页查询模型
    """
    pass


@as_query
class SetupPageQueryModel(SetupQueryModel):
    """
    接口前置操作分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSetupModel(BaseModel):
    """
    删除接口前置操作模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    setup_ids: str = Field(description='需要删除的操作ID')
