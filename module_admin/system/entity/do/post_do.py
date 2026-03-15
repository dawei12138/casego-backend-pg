from datetime import datetime
from sqlalchemy import Column, BigInteger,DateTime, Integer, String
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class SysPost(Base):
    """
    岗位信息表
    """

    __tablename__ = 'sys_post'

    post_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='岗位ID')
    post_code = Column(String(64), nullable=False, comment='岗位编码')
    post_name = Column(String(50), nullable=False, comment='岗位名称')
    post_sort = Column(Integer, nullable=False, comment='显示顺序')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')

