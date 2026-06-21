from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text

from config.base import Base


class SchemaModelGroup(Base):
    """
    JSON Schema 数据模型目录表
    """

    __tablename__ = 'schema_model_groups'
    __table_args__ = (
        Index('ix_schema_model_groups_project_id', 'project_id'),
        Index('ix_schema_model_groups_parent_id', 'parent_id'),
        Index('ix_schema_model_groups_branch_id', 'branch_id'),
        {'comment': 'JSON Schema 数据模型目录表'},
    )

    group_id = Column(String(64), primary_key=True, nullable=False, comment='目录ID')
    project_id = Column(Integer, nullable=False, comment='所属项目ID')
    branch_id = Column(String(64), nullable=True, comment='所属分支ID')
    parent_id = Column(String(64), nullable=True, comment='父目录ID')
    name = Column(String(128), nullable=False, comment='目录名称')
    create_by = Column(String(64), nullable=True, comment='')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='')
    update_time = Column(DateTime, nullable=True, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='')
    description = Column(Text, nullable=True, comment='')
    sort_no = Column(Float, nullable=True, default=0, comment='排序号')
    del_flag = Column(String(1), nullable=True, default='0', comment='')
