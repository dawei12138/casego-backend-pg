from sqlalchemy import Float, Integer, String, Text, Enum, DateTime, Column
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from module_app.enums import PlatformEnum, StepErrorEnum, ConditionTypeEnum, BoolFlagEnum


class AppSteps(Base):
    """
    测试步骤表
    """

    __tablename__ = 'app_steps'
    __table_args__ = {'comment': '测试步骤表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    case_id = Column(Integer, index=True, comment='所属测试用例ID')
    project_id = Column(Integer, index=True, comment='所属项目ID')
    parent_id = Column(Integer, default=0, comment='父级步骤ID(用于条件分支)')
    step_type = Column(String(50), comment='步骤类型: click/sendKeys/swipe/getText等')
    content = Column(Text, nullable=True, comment='输入内容/操作参数')
    text = Column(Text, nullable=True, comment='附加信息(JSON格式)')
    platform = Column(Enum(PlatformEnum, name="PlatformEnum", ), nullable=False, default=PlatformEnum.ANDROID,
                      comment='平台类型')
    error = Column(Enum(StepErrorEnum, name="StepErrorEnum"), nullable=False, default=StepErrorEnum.SHUTDOWN, comment='异常处理方式')
    condition_type = Column(Enum(ConditionTypeEnum, name="ConditionTypeEnum"), nullable=False, default=ConditionTypeEnum.NONE, comment='条件类型')
    disabled = Column(Enum(BoolFlagEnum, name="BoolFlagEnum"), nullable=False, default=BoolFlagEnum.NO, comment='是否禁用')
