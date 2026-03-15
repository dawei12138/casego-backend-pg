from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional, List, Dict

from config.enums import DataTypeEnum
from module_admin.annotation.pydantic_annotation import as_query


class FileConfig(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    file_id: Optional[int] = Field(default=None, description='表单值')
    file_name: Optional[str] = Field(default=None, description='表单值')
    file_path: Optional[str] = Field(default=None, description='表单值')
    file_size: Optional[int] = Field(default=None, description='表单值')
    mime_type: Optional[str] = Field(default=None, description='表单值')


class FormdataModel(BaseModel):
    """
    接口单body表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    formdata_id: Optional[int] = Field(default=None, description='ID')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    key: Optional[str] = Field(default=None, description='键名')
    value: Optional[str] = Field(default=None, description='表单值')
    is_run: Optional[int] = Field(default=None, description='是否启用该表单值')
    is_required: Optional[int] = Field(default=None, description='是否必填')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    data_type: Optional[DataTypeEnum] = Field(default=DataTypeEnum.STRING, description='数据类型枚举')
    # file_path: Optional[str] = Field(default=None, description='文件路径(用于文件上传)')
    form_file_config: Optional[List[FileConfig]] = Field(default=[], description='formdata的文件配置')

    @NotBlank(field_name='case_id', message='关联的测试用例ID不能为空')
    def get_case_id(self):
        return self.case_id

    def validate_fields(self):
        self.get_case_id()


class FormdataQueryModel(FormdataModel):
    """
    接口单body不分页查询模型
    """
    pass


@as_query
class FormdataPageQueryModel(FormdataQueryModel):
    """
    接口单body分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteFormdataModel(BaseModel):
    """
    删除接口单body模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    formdata_ids: str = Field(description='需要删除的ID')
