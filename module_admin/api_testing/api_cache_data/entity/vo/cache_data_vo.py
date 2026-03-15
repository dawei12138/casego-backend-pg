from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, Any
from module_admin.annotation.pydantic_annotation import as_query


class Cache_dataModel(BaseModel):
    """
    环境缓存表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[Any] = Field(default=None, description='缓存数据ID')
    cache_key: Optional[Any] = Field(default=None, description='缓存键名')
    environment_id: Optional[int] = Field(default=None, description='关联的环境ID')
    cache_value: Optional[Any] = Field(default=None, description='缓存值')
    source_type: Optional[str] = Field(default=None, description='数据来源可以为空')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    user_id: str | int | None = Field(default=None, description='用户id')


class Cache_dataQueryModel(Cache_dataModel):
    """
    环境缓存不分页查询模型
    """
    pass


@as_query
class Cache_dataPageQueryModel(Cache_dataQueryModel):
    """
    环境缓存分页查询模型
    """

    page_num: str = Field(default=1, description='当前页码')
    page_size: str = Field(default=10, description='每页记录数')


class DeleteCache_dataModel(BaseModel):
    """
    删除环境缓存模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的缓存数据ID')


class Cache_redisModel(Cache_dataQueryModel):
    """
    redis环境缓存变量查询模型
    """

    cache_key: Optional[str] = Field(default=None, description='缓存键名')
    environment_id: Optional[int] = Field(default=None, description='关联的环境ID')
    cache_value: Optional[str] = Field(default=None, description='缓存值')
    user_id: Optional[str] = Field(default=None, description='用戶id')
