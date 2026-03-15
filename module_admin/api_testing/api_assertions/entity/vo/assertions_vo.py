from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class AssertionsModel(BaseModel):
    """
    接口断言表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    assertion_id: Optional[int] = Field(default=None, description='断言ID')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    jsonpath: Optional[str] = Field(default=None, description='JSONPath表达式OR提取方法')
    jsonpath_index: Optional[int] = Field(default=None, description='JSONPath提取索引')
    extract_index_is_run: Optional[int] = Field(default=None, description='是否执行提取索引操作')
    assertion_method: Optional[str] = Field(default=None, description='断言 (==, !=, >等)')
    value: Optional[str] = Field(default=None, description='预期值')
    assert_type: Optional[str] = Field(default=None, description='断言类型 (可选)')
    is_run: Optional[int] = Field(default=None, description='是否执行该断言')
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


    def validate_fields(self):
        self.get_case_id()




class AssertionsQueryModel(AssertionsModel):
    """
    接口断言不分页查询模型
    """
    pass


@as_query
class AssertionsPageQueryModel(AssertionsQueryModel):
    """
    接口断言分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAssertionsModel(BaseModel):
    """
    删除接口断言模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    assertion_ids: str = Field(description='需要删除的断言ID')
