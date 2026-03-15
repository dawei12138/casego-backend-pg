from sqlalchemy import Integer, BigInteger, Float, DateTime, Enum, String, Column
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from module_app.enums import AgentStatusEnum


class AppAgents(Base):
    """
    Agent代理表
    """

    __tablename__ = 'app_agents'
    __table_args__ = {'comment': 'Agent代理表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(255), nullable=False, comment='Agent名称')
    host = Column(String(255), nullable=False, comment='Agent的IP地址')
    port = Column(Integer, nullable=False, comment='Agent的端口')
    secret_key = Column(String(255), nullable=True, default='', comment='Agent的密钥')
    status = Column(Enum(AgentStatusEnum, name="AgentStatusEnum"), nullable=False, default=AgentStatusEnum.OFFLINE, comment='Agent状态')
    system_type = Column(String(50), nullable=False, default='', comment='Agent系统类型: windows/linux/macos')
    version = Column(String(50), nullable=True, default='', comment='Agent端代码版本')
    lock_version = Column(BigInteger, nullable=False, default=0, comment='乐观锁版本号')
    high_temp = Column(Integer, nullable=False, default=45, comment='高温预警阈值(摄氏度)')
    high_temp_time = Column(Integer, nullable=False, default=15, comment='高温持续时间阈值(分钟)')
    has_hub = Column(Integer, nullable=False, default=0, comment='是否使用Sonic Hub: 0否 1是')




