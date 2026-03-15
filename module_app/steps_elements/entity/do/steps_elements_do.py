from sqlalchemy import Float, Integer, DateTime, String, Column
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class AppStepsElements(Base):
    """
    步骤-元素关联表
    """

    __tablename__ = 'app_steps_elements'
    __table_args__ = {'comment': '步骤-元素关联表'}

    # 联合主键
    steps_id = Column(Integer, primary_key=True, comment='步骤ID')
    elements_id = Column(Integer, comment='元素ID')




