from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Integer, LargeBinary, String, CHAR
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class SysNotice(Base):
    """
    通知公告表
    """

    __tablename__ = 'sys_notice'

    notice_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='公告ID')
    notice_title = Column(String(50), nullable=False, comment='公告标题')
    notice_type = Column(CHAR(1), nullable=False, comment='公告类型（1通知 2公告）')
    notice_content = Column(LargeBinary, comment='公告内容')
    status = Column(CHAR(1), default='0', comment='公告状态（0正常 1关闭）')

