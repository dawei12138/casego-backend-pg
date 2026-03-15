from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Integer, String, Float
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class SysMenu(Base):
    """
    菜单权限表
    """

    __tablename__ = 'sys_menu'

    menu_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='菜单ID')
    menu_name = Column(String(50), nullable=False, default='', comment='菜单名称')
    parent_id = Column(Integer, default=0, comment='父菜单ID')
    order_num = Column(Float, nullable=True, default=None, comment='排序值')
    path = Column(String(200), nullable=True, default='', comment='路由地址')
    component = Column(String(255), nullable=True, default=None, comment='组件路径')
    query = Column(String(255), nullable=True, default=None, comment='路由参数')
    route_name = Column(String(50), nullable=True, default='', comment='路由名称')
    is_frame = Column(Integer, default=1, comment='是否为外链（0是 1否）')
    is_cache = Column(Integer, default=0, comment='是否缓存（0缓存 1不缓存）')
    menu_type = Column(String(1), nullable=True, default='', comment='菜单类型（M目录 C菜单 F按钮）')
    visible = Column(String(1), nullable=True, default='0', comment='菜单状态（0显示 1隐藏）')
    status = Column(String(1), nullable=True, default='0', comment='菜单状态（0正常 1停用）')
    perms = Column(String(100), nullable=True, default=None, comment='权限标识')
    icon = Column(String(100), nullable=True, default='#', comment='菜单图标')

