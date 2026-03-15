from sqlalchemy import String, DateTime, Column, Enum, Integer, BigInteger, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiProjectSubmodules(Base):
    __tablename__ = 'api_project_submodules'
    __table_args__ = (
        # 优化按项目ID + 类型 + 删除标记查询模块
        Index('idx_submodules_project_type', 'project_id', 'type', 'del_flag'),
        # 优化按父ID查询子模块
        Index('idx_submodules_parent', 'parent_id'),
        {'comment': '项目模块表'}
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='ID')
    name = Column(String(100), nullable=True, comment='模块名称')
    type = Column(String(100), nullable=True, comment='模块类型')
    parent_id = Column(BigInteger, nullable=True, comment='父id')
    ancestors = Column(String(50), nullable=True, comment='祖级列表')
    project_id = Column(BigInteger, nullable=True, comment='所属项目id')
