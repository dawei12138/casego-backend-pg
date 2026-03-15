from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class FileModel(BaseModel):
    """
    附件管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    file_id: Optional[int] = Field(default=None, description='（主键）')
    original_name: Optional[str] = Field(default=None, description='文件原始名称')
    stored_name: Optional[str] = Field(default=None, description='文件存储名称')
    file_ext: Optional[str] = Field(default=None, description='文件扩展名')
    mime_type: Optional[str] = Field(default=None, description='文件 MIME 类型')
    file_size: Optional[int] = Field(default=None, description='文件大小（字节）')
    file_path: Optional[str] = Field(default=None, description='文件存储路径')
    file_url: Optional[str] = Field(default=None, description='文件访问 URL')
    storage_type: Optional[str] = Field(default=None, description='存储位置类型')
    is_temp: Optional[int] = Field(default=None, description='是否临时文件')
    file_hash: Optional[str] = Field(default=None, description='文件哈希值')
    biz_tag: Optional[str] = Field(default=None, description='业务标签')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='stored_name', message='文件存储名称不能为空')
    def get_stored_name(self):
        return self.stored_name


    def validate_fields(self):
        self.get_stored_name()




class FileQueryModel(FileModel):
    """
    附件管理不分页查询模型
    """
    pass


@as_query
class FilePageQueryModel(FileQueryModel):
    """
    附件管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteFileModel(BaseModel):
    """
    删除附件管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    file_ids: str = Field(description='需要删除的')
