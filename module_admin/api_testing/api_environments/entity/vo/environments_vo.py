from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional, Dict, Any, List
from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataModel


class HeaderItemModel(BaseModel):
    """
    请求头项模型
    """
    key: str = Field(..., description="请求头的键", json_schema_extra={"example": "Content-Type"})
    value: str = Field(..., description="请求头的值", example="application/json")
    description: Optional[str] = Field(None, description="请求头描述")
    is_run: Optional[bool] = Field(True, description="是否启用该请求头")


class CookieItemModel(BaseModel):
    """
    Cookie项模型
    """
    key: str = Field(..., description="Cookie的键", json_schema_extra={"example": "session_id"})
    value: str = Field(default="", description="Cookie的值", example="abc123")
    description: Optional[str] = Field(None, description="Cookie描述")
    is_run: Optional[bool] = Field(True, description="是否启用该Cookie")


class EnvironmentsModel(BaseModel):
    """
    环境配置表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='环境ID')
    name: Optional[str] = Field(default=None, description='环境名称')
    project_id: Optional[int] = Field(default=None, description='所属项目ID')
    is_default: Optional[int] = Field(default=None, description='是否为默认环境')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    request_timeout: Optional[int] = Field(
        default=5000,
        description="请求超时(ms)，必须大于0",
        example=5000
    )
    global_headers: Optional[List[HeaderItemModel]] = Field(
        default_factory=list,
        description="全局请求头列表",
        example=[{
            "key": "Content-Type",
            "value": "application/json",
            "description": "内容类型",
            "is_run": True
        }]
    )
    global_cookies: Optional[List[CookieItemModel]] = Field(
        default_factory=list,
        description="全局Cookies列表",
        example=[{
            "key": "session_id",
            "value": "abc123",
            "description": "会话ID",
            "is_run": True
        }]
    )

    @NotBlank(field_name='name', message='环境名称不能为空')
    def get_name(self):
        return self.name

    def validate_fields(self):
        self.get_name()


class EnvironmentsQueryModel(EnvironmentsModel):
    """
    环境配置不分页查询模型
    """
    pass


@as_query
class EnvironmentsPageQueryModel(EnvironmentsQueryModel):
    """
    环境配置分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteEnvironmentsModel(BaseModel):
    """
    删除环境配置模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的环境ID')


class EnvironmentsConfig(EnvironmentsModel):
    url: Optional[str] = Field(default=None, description='默认服务名')
    cache_list: Optional[List[dict]] = Field(default=[], description='缓存变量')
    global_headers: Optional[List[HeaderItemModel]] = Field(default=[], description='环境级别的公共请求头')
    global_cookies: Optional[List[CookieItemModel]] = Field(default=[], description='环境级别的公共Cookies')

    pass
