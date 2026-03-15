# -*- coding: utf-8 -*-
"""
Sonic/App 模块枚举类型定义
"""
from enum import IntEnum, Enum


class PlatformEnum(IntEnum):
    """平台类型枚举"""
    ANDROID = 1
    IOS = 2


class AgentStatusEnum(IntEnum):
    """Agent状态枚举"""
    OFFLINE = 0
    ONLINE = 1
    BUSY = 2


class DeviceStatusEnum(str, Enum):
    """设备状态枚举"""
    ONLINE = "ONLINE"              # 在线空闲
    OFFLINE = "OFFLINE"            # 离线
    DEBUGGING = "DEBUGGING"        # 远程调试中
    TESTING = "TESTING"            # 自动化测试中
    DISCONNECTED = "DISCONNECTED"  # 已断开


class StepErrorEnum(IntEnum):
    """步骤异常处理枚举"""
    SHUTDOWN = 0     # 终止执行
    CONTINUE = 1     # 忽略继续
    WARNING = 2      # 警告并继续


class ConditionTypeEnum(IntEnum):
    """条件类型枚举"""
    NONE = 0         # 无条件
    IF = 1           # if条件
    ELSE_IF = 2      # else if条件
    ELSE = 3         # else条件
    WHILE = 4        # while循环


class EleTypeEnum(str, Enum):
    """元素定位类型枚举"""
    ID = "id"
    XPATH = "xpath"
    ACCESSIBILITY_ID = "accessibilityId"
    NAME = "name"
    CLASS_NAME = "className"
    CSS_SELECTOR = "cssSelector"
    LINK_TEXT = "linkText"
    IMAGE = "image"
    POINT = "point"
    POCO = "poco"
    CUSTOM = "custom"


class UserSourceEnum(str, Enum):
    """用户来源枚举"""
    LOCAL = "local"
    LDAP = "ldap"
    OAUTH = "oauth"


class BoolFlagEnum(IntEnum):
    """通用布尔标志枚举"""
    NO = 0
    YES = 1
