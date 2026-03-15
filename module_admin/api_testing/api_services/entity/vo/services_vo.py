from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class ServicesModel(BaseModel):
    """
    环境服务地址表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='服务ID')
    name: Optional[str] = Field(default=None, description='服务名称')
    url: Optional[str] = Field(default=None, description='服务地址')
    environment_id: Optional[int] = Field(default=None, description='所属环境ID')
    is_default: Optional[int] = Field(default=None, description='是否为默认服务')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='name', message='服务名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='url', message='服务地址不能为空')
    def get_url(self):
        return self.url

    @NotBlank(field_name='is_default', message='是否为默认服务不能为空')
    def get_is_default(self):
        return self.is_default

    def validate_fields(self):
        self.get_name()
        self.get_url()

        self.get_is_default()


class ServicesQueryModel(ServicesModel):
    """
    环境服务地址不分页查询模型
    """
    pass


@as_query
class ServicesPageQueryModel(ServicesQueryModel):
    """
    环境服务地址分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteServicesModel(BaseModel):
    """
    删除环境服务地址模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的服务ID')
