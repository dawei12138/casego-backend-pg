from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class McpconfigModel(BaseModel):
    """
    MCP服务器配置表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    config_id: Optional[UUID] = Field(default=None, description='配置唯一标识符(UUID)')
    server_name: Optional[str] = Field(default=None, description='服务器逻辑名称，作为工具名前缀（如 playwright、fetch）')
    enabled: Optional[bool] = Field(default=None, description='是否启用此服务器')
    transport: Optional[str] = Field(default=None, description='传输类型: stdio / streamable_http / sse / websocket')
    command: Optional[str] = Field(default=None, description='stdio模式: 可执行文件路径（如 npx、python、uvx）')
    args: Optional[list] = Field(default=None, description='stdio模式: 命令行参数列表，如 ["@playwright/mcp@latest", "--headless"]')
    env: Optional[dict] = Field(default=None, description='stdio模式: 子进程环境变量字典')
    cwd: Optional[str] = Field(default=None, description='stdio模式: 子进程工作目录')
    url: Optional[str] = Field(default=None, description='streamable_http/sse/websocket模式: 远程服务器URL')
    headers: Optional[dict] = Field(default=None, description='streamable_http/sse模式: 附加HTTP请求头（如认证token）')
    timeout: Optional[int] = Field(default=None, description='请求超时时间（秒）')
    sse_read_timeout: Optional[int] = Field(default=None, description='SSE流读取超时时间（秒）')
    session_kwargs: Optional[dict] = Field(default=None, description='传递给MCP ClientSession的额外参数')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    description: Optional[str] = Field(default=None, description='')
    sort_no: Optional[float] = Field(default=None, description='')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='server_name', message='服务器逻辑名称，作为工具名前缀不能为空')
    def get_server_name(self):
        return self.server_name


    def validate_fields(self):
        self.get_server_name()




class McpconfigQueryModel(McpconfigModel):
    """
    MCP服务器配置不分页查询模型
    """
    pass


@as_query
class McpconfigPageQueryModel(McpconfigQueryModel):
    """
    MCP服务器配置分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteMcpconfigModel(BaseModel):
    """
    删除MCP服务器配置模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    config_ids: str = Field(description='需要删除的配置唯一标识符(UUID)')
