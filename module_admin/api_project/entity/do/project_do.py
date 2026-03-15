from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, BigInteger
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiProject(Base):
    """
    项目表
    """

    __tablename__ = 'api_project'
    __table_args__ = {'comment': '项目表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='ID')
    name = Column(String(100), nullable=True, comment='项目名称')
    type = Column(Enum('0', '1', '2', '3', name="ProjectTypeEnum"), nullable=True, comment='项目类型')
    parent_id = Column(BigInteger, nullable=True, comment='父部门id')
    ancestors = Column(String(50), nullable=True, comment='祖级列表')
