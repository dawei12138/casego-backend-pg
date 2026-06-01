import uuid

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer, Numeric, String, Text, Uuid
from sqlalchemy.dialects.postgresql import JSONB

from config.base import Base


class ModuleUuidDemo(Base):
    """
    UUID主键业务示例表
    """

    __tablename__ = 'module_uuid_demo'
    __table_args__ = {'comment': 'UUID主键业务示例表'}

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, nullable=False, comment='主键ID-uuid')
    title = Column(String(100), nullable=False, comment='业务标题')
    type = Column(Enum('normal', 'important', 'urgent', name='module_uuid_demo_type_enum'), nullable=True, default='normal', comment='业务类型')
    business_code = Column(String(64), nullable=True, comment='业务编号')
    customer_name = Column(String(100), nullable=True, comment='客户名称')
    status = Column(String(20), nullable=True, default='draft', comment='业务状态')
    priority = Column(Integer, nullable=True, default=0, comment='优先级')
    amount = Column(Numeric(12, 2), nullable=True, comment='业务金额')
    enabled = Column(Boolean, nullable=True, default=True, comment='是否启用')
    occurred_date = Column(Date, nullable=True, comment='发生日期')
    closed_time = Column(DateTime, nullable=True, comment='关闭时间')
    extra_info = Column(JSONB, nullable=True, comment='扩展信息')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')
    description = Column(Text, nullable=True, comment='描述')
    sort_no = Column(Integer, nullable=True, default=0, comment='排序号')
    del_flag = Column(String(1), nullable=True, default='0', comment='删除标志')
