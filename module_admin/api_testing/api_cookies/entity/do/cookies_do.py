from sqlalchemy import Text, Integer, DateTime, SmallInteger, Column, String, Float, Boolean, Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.enums import DataTypeEnum


class ApiCookies(Base):
    """
    接口请求Cookie表
    """

    __tablename__ = 'api_cookies'
    __table_args__ = {'comment': '接口请求Cookie表'}

    cookie_id = Column(Integer, primary_key=True, comment='ID')
    case_id = Column(Integer, nullable=False, comment='关联的测试用例ID')
    key = Column(String(255), nullable=False, comment='Cookie键名')
    value = Column(Text, nullable=True, comment='Cookie值')
    domain = Column(String(255), nullable=True, comment='作用域')
    path = Column(String(255), nullable=True, comment='路径')
    is_run = Column(Boolean, default=True, comment='是否启用该Cookie')
    is_required = Column(Boolean, default=False, comment='是否必填参数')
    data_type = Column(Enum(DataTypeEnum, name="DataTypeEnum"), default=DataTypeEnum.STRING, comment='数据类型')






