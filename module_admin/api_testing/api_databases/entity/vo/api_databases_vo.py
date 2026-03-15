from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class Api_databasesModel(BaseModel):
    """
    数据库配置表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='数据库ID')
    name: Optional[str] = Field(default=None, description='数据库名称')
    db_type: Optional[str] = Field(default=None, description='数据库类型（如1 MySQL、2Redis，）')
    host: Optional[str] = Field(default=None, description='数据库主机')
    port: Optional[int] = Field(default=None, description='数据库端口')
    username: Optional[str] = Field(default=None, description='数据库用户名')
    password: Optional[str] = Field(default=None, description='数据库密码')
    project_id: Optional[int] = Field(default=None, description='所属项目ID')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='name', message='数据库名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='db_type', message='数据库类型不能为空')
    def get_db_type(self):
        return self.db_type

    @NotBlank(field_name='host', message='数据库主机不能为空')
    def get_host(self):
        return self.host

    @NotBlank(field_name='port', message='数据库端口不能为空')
    def get_port(self):
        return self.port

    @NotBlank(field_name='project_id', message='所属项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    def validate_fields(self):
        self.get_name()
        self.get_db_type()
        self.get_host()
        self.get_port()
        self.get_project_id()


class Api_databasesQueryModel(Api_databasesModel):
    """
    数据库配置不分页查询模型
    """
    pass


@as_query
class Api_databasesPageQueryModel(Api_databasesQueryModel):
    """
    数据库配置分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteApi_databasesModel(BaseModel):
    """
    删除数据库配置模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的数据库ID')


class ExecuteScriptModel(BaseModel):
    """
    执行脚本请求模型
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    db_id: int = Field(description='数据库配置ID')
    script: str = Field(description='执行的SQL脚本')
    project_id: Optional[str] = Field(default=None, description='所属项目ID')
