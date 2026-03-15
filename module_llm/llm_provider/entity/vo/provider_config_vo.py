from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class Provider_configModel(BaseModel):
    """
    LLM提供商配置表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    provider_id: Optional[int] = Field(default=None, description='提供商配置ID')
    provider_key: Optional[str] = Field(default=None, description='提供商标识(如openai/anthropic/google等)')
    provider_name: Optional[str] = Field(default=None, description='提供商显示名称(如OpenAI/Anthropic/Google等)')
    api_key: Optional[str] = Field(default=None, description='API密钥(建议加密存储)')
    api_secret: Optional[str] = Field(default=None, description='API密钥对(部分提供商需要)')
    base_url: Optional[str] = Field(default=None, description='API基础URL(自定义或代理时使用)')
    api_version: Optional[str] = Field(default=None, description='API版本(Azure等需要)')
    timeout: Optional[int] = Field(default=None, description='请求超时时间(秒)')
    max_retries: Optional[int] = Field(default=None, description='最大重试次数')
    extra_headers: Optional[dict] = Field(default=None, description='额外请求头(JSON格式)')
    icon_url: Optional[str] = Field(default=None, description='提供商图标URL')
    status: Optional[str] = Field(default=None, description='状态（0禁用 1启用）')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')


class Provider_configQueryModel(Provider_configModel):
    """
    LLM提供商配置不分页查询模型
    """
    pass


@as_query
class Provider_configPageQueryModel(Provider_configQueryModel):
    """
    LLM提供商配置分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProvider_configModel(BaseModel):
    """
    删除LLM提供商配置模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    provider_ids: str = Field(description='需要删除的提供商配置ID')
