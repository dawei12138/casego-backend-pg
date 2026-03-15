from sqlalchemy import Integer, Column, DateTime, Enum, Text, Float, String
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from module_app.enums import EleTypeEnum


class AppElements(Base):
    """
    控件元素表
    """

    __tablename__ = 'app_elements'
    __table_args__ = {'comment': '控件元素表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    ele_name = Column(String(255), nullable=True, comment='元素名称')
    ele_type = Column(Enum(EleTypeEnum, name="EleTypeEnum"), nullable=True, default=EleTypeEnum.ID, comment='定位类型')
    ele_value = Column(Text, nullable=True, comment='定位值')
    project_id = Column(Integer, nullable=True, index=True, comment='所属项目ID')
    module_id = Column(Integer, nullable=True, default=0, index=True, comment='所属模块ID')




