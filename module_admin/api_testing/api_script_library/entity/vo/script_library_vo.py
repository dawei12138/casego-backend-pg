from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query

from enum import Enum as PyEnum


class ScriptTypeEnum(str, PyEnum):
    """脚本类型枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"


class Script_libraryModel(BaseModel):
    """
    公共脚本库表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    script_id: Optional[int] = Field(default=None, description='脚本ID')
    script_name: Optional[str] = Field(default=None, description='脚本名称')
    script_type: Optional[ScriptTypeEnum] = Field(default=None, description='脚本类型(python/javascript)')
    script_content: Optional[str] = Field(default=None, description='脚本内容')
    status: Optional[int] = Field(default=None, description='状态(0停用 1正常)')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')


class Script_libraryQueryModel(Script_libraryModel):
    """
    公共脚本库不分页查询模型
    """
    pass


@as_query
class Script_libraryPageQueryModel(Script_libraryQueryModel):
    """
    公共脚本库分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteScript_libraryModel(BaseModel):
    """
    删除公共脚本库模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    script_ids: str = Field(description='需要删除的脚本ID')


class ExecuteScriptRequestModel(BaseModel):
    """
    执行脚本请求模型
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    script_id: Optional[int] = Field(default=None, description='脚本ID（通过ID执行已保存的脚本）')
    script_content: Optional[str] = Field(default=None, description='脚本内容（直接执行传入的脚本）')
    script_type: Optional[ScriptTypeEnum] = Field(default=None, description='脚本类型')
    env_id: Optional[int] = Field(default=0, description='环境ID')


class ExecuteScriptResponseModel(BaseModel):
    """
    执行脚本响应模型
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    success: bool = Field(description='是否执行成功')
    result: Optional[str] = Field(default=None, description='执行结果')
    logs: Optional[str] = Field(default=None, description='执行日志')
    error: Optional[str] = Field(default=None, description='错误信息')
