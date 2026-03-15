from sqlalchemy import String, Column, Text, Integer, DateTime, Float, SmallInteger, Boolean, Enum, JSON
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.enums import DataTypeEnum
from sqlalchemy.dialects.postgresql import JSONB

class ApiFormdata(Base):
    """
    接口单body表
    """

    __tablename__ = 'api_formdata'
    __table_args__ = {'comment': '接口表单body'}

    formdata_id = Column(Integer, primary_key=True, comment='ID')
    case_id = Column(Integer, nullable=False, comment='关联的测试用例ID')
    key = Column(String(255), nullable=False, comment='键名')
    value = Column(Text, nullable=True, comment='表单值')
    is_run = Column(Boolean, default=True, comment='是否启用该表单值')
    is_required = Column(Boolean, default=False, comment='是否必填')
    data_type = Column(Enum(DataTypeEnum, name="DataTypeEnum"), default=DataTypeEnum.STRING, comment='数据类型')
    # file_path = Column(String(512), nullable=True, comment='文件路径')
    form_file_config = Column(JSONB, default=[], comment='formdata的文件配置')
