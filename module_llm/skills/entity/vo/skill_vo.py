from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank

from module_admin.annotation.pydantic_annotation import as_query


class SkillModel(BaseModel):
    """Skill metadata model."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    skill_id: Optional[UUID] = Field(default=None, description='Skill UUID')
    skill_name: Optional[str] = Field(default=None, description='Skill directory name')
    display_name: Optional[str] = Field(default=None, description='Display name')
    description: Optional[str] = Field(default=None, description='Description')
    enabled: Optional[bool] = Field(default=None, description='Enabled flag')
    source_type: Optional[str] = Field(default=None, description='Source type: manual/upload/url')
    source_url: Optional[str] = Field(default=None, description='Source URL')
    allowed_tools: Optional[str] = Field(default=None, description='Allowed tools list')
    license_info: Optional[str] = Field(default=None, description='License info')
    create_by: Optional[str] = Field(default=None, description='Creator')
    create_time: Optional[datetime] = Field(default=None, description='Create time')
    update_by: Optional[str] = Field(default=None, description='Updater')
    update_time: Optional[datetime] = Field(default=None, description='Update time')
    remark: Optional[str] = Field(default=None, description='Remark')
    sort_no: Optional[float] = Field(default=None, description='Sort number')
    del_flag: Optional[str] = Field(default=None, description='Delete flag')

    @NotBlank(field_name='skill_name', message='skill_name cannot be empty')
    def get_skill_name(self):
        return self.skill_name

    def validate_fields(self):
        self.get_skill_name()


class SkillQueryModel(SkillModel):
    """Skill query model (non-paged)."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)


@as_query
class SkillPageQueryModel(SkillQueryModel):
    """Skill page query model."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    page_num: int = Field(default=1, description='Page number')
    page_size: int = Field(default=10, description='Page size')


class DeleteSkillModel(BaseModel):
    """Delete skill request model."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    skill_ids: str = Field(description='Comma-separated skill UUIDs')


class SkillFileModel(BaseModel):
    """Skill file model."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    file_id: Optional[UUID] = Field(default=None, description='File UUID')
    skill_id: Optional[UUID] = Field(default=None, description='Skill UUID')
    file_path: Optional[str] = Field(default=None, description='Relative file path')
    content: Optional[str] = Field(default=None, description='File content')
    is_binary: Optional[bool] = Field(default=False, description='Binary file flag')
    create_by: Optional[str] = Field(default=None, description='Creator')
    create_time: Optional[datetime] = Field(default=None, description='Create time')
    update_by: Optional[str] = Field(default=None, description='Updater')
    update_time: Optional[datetime] = Field(default=None, description='Update time')
    del_flag: Optional[str] = Field(default=None, description='Delete flag')


class SkillDetailModel(SkillModel):
    """Skill detail model with file list."""

    files: Optional[List[SkillFileModel]] = Field(default=None, description='Skill files')


class SkillImportUrlModel(BaseModel):
    """Import skill from URL."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    url: str = Field(description='Import URL')
    skill_name: Optional[str] = Field(default=None, description='Optional skill directory name')


class SkillFileContentSaveModel(BaseModel):
    """Save single skill file content (upsert by file_path)."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    file_path: str = Field(description='Relative file path inside skill directory')
    content: str = Field(default='', description='File text content')
    is_binary: Optional[bool] = Field(default=False, description='Binary file flag')
    sync_all: Optional[bool] = Field(default=False, description='Whether to run full skills sync after save')


class SkillFilesBatchSaveModel(BaseModel):
    """Save batch skill file content."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    files: List[SkillFileContentSaveModel] = Field(default_factory=list, description='Files to save')
    sync_all: Optional[bool] = Field(default=False, description='Whether to run full skills sync after save')


class SkillFolderCreateModel(BaseModel):
    """Create a subfolder inside a skill directory."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    folder_path: str = Field(description='Relative folder path to create (e.g. "references" or "references/sub")')


class SkillFolderRenameModel(BaseModel):
    """Rename a subfolder inside a skill directory."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    old_path: str = Field(description='Current relative folder path')
    new_path: str = Field(description='New relative folder path')


class SkillFolderDeleteModel(BaseModel):
    """Delete a subfolder and all files inside it."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    folder_path: str = Field(description='Relative folder path to delete')


class SkillFileMoveModel(BaseModel):
    """Move a file to a new path within the same skill."""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    old_path: str = Field(description='Current relative file path')
    new_path: str = Field(description='New relative file path')