from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Integer, String
from sqlalchemy.orm import relationship
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class GenTable(Base):
    """
    代码生成业务表
    """

    __tablename__ = 'gen_table'

    table_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='编号')
    table_name = Column(String(200), nullable=True, default='', comment='表名称')
    table_comment = Column(String(500), nullable=True, default='', comment='表描述')
    sub_table_name = Column(String(64), nullable=True, comment='关联子表的表名')
    sub_table_fk_name = Column(String(64), nullable=True, comment='子表关联的外键名')
    class_name = Column(String(100), nullable=True, default='', comment='实体类名称')
    tpl_category = Column(String(200), nullable=True, default='crud', comment='使用的模板（crud单表操作 tree树表操作）')
    tpl_web_type = Column(
        String(30), nullable=True, default='', comment='前端模板类型（element-ui模版 element-plus模版）'
    )
    package_name = Column(String(100), nullable=True, comment='生成包路径')
    module_name = Column(String(30), nullable=True, comment='生成模块名')
    business_name = Column(String(30), nullable=True, comment='生成业务名')
    function_name = Column(String(100), nullable=True, comment='生成功能名')
    function_author = Column(String(100), nullable=True, comment='生成功能作者')
    gen_type = Column(String(1), nullable=True, default='0', comment='生成代码方式（0zip压缩包 1自定义路径）')
    gen_path = Column(String(200), nullable=True, default='/', comment='生成路径（不填默认项目路径）')
    options = Column(String(1000), nullable=True, comment='其它生成选项')

    columns = relationship(
        'GenTableColumn',
        order_by='GenTableColumn.sort',
        back_populates='tables',
        primaryjoin='GenTable.table_id == GenTableColumn.table_id',
        foreign_keys='GenTableColumn.table_id'
    )


class GenTableColumn(Base):
    """
    代码生成业务表字段
    """

    __tablename__ = 'gen_table_column'

    column_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='编号')
    table_id = Column(BigInteger, nullable=True, index=True, comment='归属表编号')
    column_name = Column(String(200), nullable=True, comment='列名称')
    column_comment = Column(String(500), nullable=True, comment='列描述')
    column_type = Column(String(500), nullable=True, comment='列类型')
    python_type = Column(String(500), nullable=True, comment='PYTHON类型')
    python_field = Column(String(200), nullable=True, comment='PYTHON字段名')
    is_pk = Column(String(1), nullable=True, comment='是否主键（1是）')
    is_increment = Column(String(1), nullable=True, comment='是否自增（1是）')
    is_required = Column(String(1), nullable=True, comment='是否必填（1是）')
    is_unique = Column(String(1), nullable=True, comment='是否唯一（1是）')
    is_insert = Column(String(1), nullable=True, comment='是否为插入字段（1是）')
    is_edit = Column(String(1), nullable=True, comment='是否编辑字段（1是）')
    is_list = Column(String(1), nullable=True, comment='是否列表字段（1是）')
    is_query = Column(String(1), nullable=True, comment='是否查询字段（1是）')
    query_type = Column(String(200), nullable=True, default='EQ', comment='查询方式（等于、不等于、大于、小于、范围）')
    html_type = Column(
        String(200), nullable=True, comment='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）'
    )
    dict_type = Column(String(200), nullable=True, default='', comment='字典类型')
    sort = Column(Integer, nullable=True, comment='排序')

    tables = relationship(
        'GenTable',
        back_populates='columns',
        primaryjoin='GenTableColumn.table_id == GenTable.table_id',
        foreign_keys=[table_id]
    )
