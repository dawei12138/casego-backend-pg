from datetime import datetime
from sqlalchemy import Column, BigInteger,DateTime, Integer, String
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class SysRole(Base):
    """
    角色信息表
    """

    __tablename__ = 'sys_role'

    role_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='角色ID')
    role_name = Column(String(30), nullable=False, comment='角色名称')
    role_key = Column(String(100), nullable=False, comment='角色权限字符串')
    role_sort = Column(Integer, nullable=False, comment='显示顺序')
    data_scope = Column(
        String(1),
        default='1',
        comment='数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）',
    )
    menu_check_strictly = Column(Integer, default=1, comment='菜单树选择项是否关联显示')
    dept_check_strictly = Column(Integer, default=1, comment='部门树选择项是否关联显示')
    status = Column(String(1), nullable=False, default='0', comment='角色状态（0正常 1停用）')



class SysRoleDept(Base):
    """
    角色和部门关联表
    """

    __tablename__ = 'sys_role_dept'

    role_id = Column(BigInteger, primary_key=True, nullable=False, comment='角色ID')
    dept_id = Column(BigInteger, primary_key=True, nullable=False, comment='部门ID')


class SysRoleMenu(Base):
    """
    角色和菜单关联表
    """

    __tablename__ = 'sys_role_menu'

    role_id = Column(BigInteger, primary_key=True, nullable=False, comment='角色ID')
    menu_id = Column(BigInteger, primary_key=True, nullable=False, comment='菜单ID')
