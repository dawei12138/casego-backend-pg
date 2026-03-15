from sqlalchemy import Text, Integer, DateTime, SmallInteger, Column, String, Float, Boolean, Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.enums import DataTypeEnum


class ApiParams(Base):
    """
    接口请求参数表
    """

    __tablename__ = 'api_params'
    __table_args__ = {'comment': '接口请求参数表'}

    param_id = Column(Integer, primary_key=True, comment='ID')
    case_id = Column(Integer, nullable=False, comment='关联的测试用例ID')
    key = Column(String(255), nullable=False, comment='参数键名')
    value = Column(Text, nullable=True, comment='参数值')
    is_run = Column(Boolean, default=True, comment='是否启用该参数')
    is_required = Column(Boolean, default=True, comment='是否必填参数')
    description = Column(String(255), nullable=True, comment='描述')
    data_type = Column(Enum(DataTypeEnum, name="DataTypeEnum"), default=DataTypeEnum.STRING, comment='数据类型')




