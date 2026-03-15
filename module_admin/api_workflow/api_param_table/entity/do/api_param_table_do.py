from sqlalchemy import Column, Float, String, BigInteger, DateTime, Integer
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiParamTable(Base):
    __tablename__ = "api_param_table"
    __table_args__ = (
        {'comment': '参数化数据表主表'},
    )

    parameterization_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    workflow_id = Column(BigInteger, nullable=True, comment='所属执行器ID')
    name = Column(String(100), comment='参数表名称')



