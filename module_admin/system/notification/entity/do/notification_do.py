from sqlalchemy import SmallInteger, Float, Integer, Column, String, BigInteger, JSON, Text, DateTime, Enum, Boolean, \
    Index
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.enums import NotificationType


class ApiNotification(Base):
    __tablename__ = "api_notification"
    __table_args__ = (
        Index('ix_notification_user_id', 'user_id'),
        Index('ix_notification_is_read', 'is_read'),
        Index('ix_notification_type', 'notification_type'),
        {
            'comment': '通知消息表'
        }
    )

    notification_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='通知ID')
    user_id = Column(BigInteger, nullable=False, comment="接收用户ID")

    # 通知基本信息
    notification_type = Column(Enum(NotificationType, name="NotificationType"), nullable=True, comment="通知类型(system/task/workflow/alert)")
    title = Column(String(200), nullable=True, comment="通知标题")
    message = Column(Text, nullable=True, comment="通知内容")

    # 状态
    is_read = Column(Boolean, nullable=True, comment="是否已读")
    read_time = Column(DateTime, comment="阅读时间")

    # 关联业务
    business_type = Column(String(50), nullable=True, comment="关联业务类型(workflow/test_case/report等)")
    business_id = Column(BigInteger, nullable=True, comment="关联业务ID")

    # 扩展数据
    extra_data = Column(JSONB, nullable=True, comment="扩展数据")




