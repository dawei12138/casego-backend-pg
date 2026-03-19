from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional, List
from module_admin.annotation.pydantic_annotation import as_query


class SkillModel(BaseModel):
    """
    AI技能配置表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    skill_id: Optional[UUID] = Field(default=None, description='技能唯一标识符(UUID)')
    skill_name: Optional[str] = Field(default=None, description='技能目录名（英文标识符）')
    display_name: Optional[str] = Field(default=None, description='技能显示名称')
    description: Optional[str] = Field(default=None, description='技能描述')
    enabled: Optional[bool] = Field(default=None, description='是否启用')
    source_type: Optional[str] = Field(default=None, description='来源类型: manual / upload / url')
    source_url: Optional[str] = Field(default=None, description='URL导入源地址')
    allowed_tools: Optional[str] = Field(default=None, description='允许的工具列表')
    license_info: Optional[str] = Field(default=None, description='许可证信息')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    sort_no: Optional[float] = Field(default=None, description='')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='skill_name', message='技能目录名不能为空')
    def get_skill_name(self):
        return self.skill_name

    def validate_fields(self):
        self.get_skill_name()


class SkillQueryModel(SkillModel):
    """
    技能不分页查询模型
    """
    pass


@as_query
class SkillPageQueryModel(SkillQueryModel):
    """
    技能分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSkillModel(BaseModel):
    """
    删除技能模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    skill_ids: str = Field(description='需要删除的技能ID，多个逗号分隔')


class SkillFileModel(BaseModel):
    """
    技能文件对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    file_id: Optional[UUID] = Field(default=None, description='文件唯一标识符(UUID)')
    skill_id: Optional[UUID] = Field(default=None, description='所属技能ID')
    file_path: Optional[str] = Field(default=None, description='文件相对路径')
    content: Optional[str] = Field(default=None, description='文件内容')
    is_binary: Optional[bool] = Field(default=False, description='是否二进制文件')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    del_flag: Optional[str] = Field(default=None, description='')


class SkillDetailModel(SkillModel):
    """
    技能详情（含文件列表）
    """
    files: Optional[List[SkillFileModel]] = Field(default=None, description='技能文件列表')


class SkillImportUrlModel(BaseModel):
    """
    URL导入模型
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    url: str = Field(description='导入URL地址')
    skill_name: Optional[str] = Field(default=None, description='技能目录名（可选，自动从URL推断）')
