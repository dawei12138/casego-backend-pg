from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query
from module_app.enums import PlatformEnum


class CasesModel(BaseModel):
    """
    测试用例表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='主键ID')
    name: Optional[str] = Field(default=None, description='用例名称')
    des: Optional[str] = Field(default=None, description='用例描述')
    designer: Optional[str] = Field(default=None, description='设计者')
    platform: Optional[PlatformEnum] = Field(default=None, description='平台类型')
    project_id: Optional[int] = Field(default=None, description='所属项目ID')
    module_id: Optional[int] = Field(default=None, description='所属模块ID')
    version: Optional[str] = Field(default=None, description='版本号')
    edit_time: Optional[datetime] = Field(default=None, description='最后编辑时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='name', message='用例名称不能为空')
    def get_name(self):
        return self.name


    @NotBlank(field_name='project_id', message='所属项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    def validate_fields(self):
        self.get_name()
        self.get_project_id()


class CasesQueryModel(CasesModel):
    """
    测试用例不分页查询模型
    """
    pass


@as_query
class CasesPageQueryModel(CasesQueryModel):
    """
    测试用例分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteCasesModel(BaseModel):
    """
    删除测试用例模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID')
