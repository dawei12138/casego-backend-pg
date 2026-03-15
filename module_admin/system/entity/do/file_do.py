from sqlalchemy import BigInteger, DateTime, SmallInteger, String, Float, Column, Text, Integer, Boolean
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class SysFile(Base):
    """
    文件存储表（仅业务字段）
    """
    __tablename__ = 'sys_file'
    __table_args__ = {'comment': '附件表'}
    file_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='（主键）')
    # 文件原始名称（上传时的文件名）
    original_name = Column(String(255), nullable=True, comment="文件原始名称")
    # 文件存储名称（系统生成的唯一文件名，例如 UUID）
    stored_name = Column(String(191), nullable=False, unique=True, comment="文件存储名称")
    # 文件扩展名（不带 . 号）
    file_ext = Column(String(50), nullable=True, comment="文件扩展名")
    # MIME 类型（如 image/png, application/pdf）
    mime_type = Column(String(100), nullable=True, comment="文件 MIME 类型")
    # 文件大小（字节）
    file_size = Column(BigInteger, nullable=True, comment="文件大小（字节）")
    # 文件存储路径（相对路径或绝对路径）
    file_path = Column(Text, nullable=True, comment="文件存储路径")
    # 文件访问 URL（CDN 地址或拼接后的访问链接）
    file_url = Column(Text, nullable=True, comment="文件访问 URL")
    # 存储位置（本地、OSS、S3、FTP...）
    storage_type = Column(String(50), default="local", comment="存储位置类型")
    # 是否是临时文件（例如用于导出、缓存）
    is_temp = Column(Boolean, default=False, comment="是否临时文件")
    # 文件哈希（如 md5/sha256，用于秒传和校验完整性）
    file_hash = Column(String(128), nullable=True, comment="文件哈希值")
    # 业务标签（如 avatar, contract, report）
    biz_tag = Column(String(100), nullable=True, comment="业务标签")



