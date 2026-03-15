from datetime import datetime
from sqlalchemy import Column, BigInteger,DateTime, Integer, String
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class SysUser(Base):
    """
    用户信息表
    """

    __tablename__ = 'sys_user'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    dept_id = Column(Integer, default=None, comment='部门ID')
    user_name = Column(String(30), nullable=False, comment='用户账号')
    nick_name = Column(String(30), nullable=False, comment='用户昵称')
    user_type = Column(String(2), default='00', comment='用户类型（00系统用户）')
    email = Column(String(50), default='', comment='用户邮箱')
    phonenumber = Column(String(11), default='', comment='手机号码')
    sex = Column(String(1), default='0', comment='用户性别（0男 1女 2未知）')
    avatar = Column(String(100), default='', comment='头像地址')
    password = Column(String(100), default='', comment='密码')
    status = Column(String(1), default='0', comment='帐号状态（0正常 1停用）')
    login_ip = Column(String(128), default='', comment='最后登录IP')
    login_date = Column(DateTime, comment='最后登录时间')



class SysUserRole(Base):
    """
    用户和角色关联表
    """

    __tablename__ = 'sys_user_role'

    user_id = Column(BigInteger, primary_key=True, nullable=False, comment='用户ID')
    role_id = Column(BigInteger, primary_key=True, nullable=False, comment='角色ID')


class SysUserPost(Base):
    """
    用户与岗位关联表
    """

    __tablename__ = 'sys_user_post'

    user_id = Column(BigInteger, primary_key=True, nullable=False, comment='用户ID')
    post_id = Column(BigInteger, primary_key=True, nullable=False, comment='岗位ID')
