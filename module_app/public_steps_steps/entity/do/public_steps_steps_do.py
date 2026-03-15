from sqlalchemy import DateTime, Column, String, Float, Integer
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class AppPublicStepsSteps(Base):
    """
    公共步骤-步骤关联表 - 多对多关系映射
    """

    __tablename__ = 'app_public_steps_steps'
    __table_args__ = {'comment': '公共步骤-步骤关联表'}

    # 联合主键
    public_steps_id = Column(Integer, primary_key=True, nullable=False, comment='公共步骤ID')
    steps_id = Column(Integer, comment='步骤ID')



