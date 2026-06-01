import enum


class ModuleUuidDemoTypeEnum(str, enum.Enum):
    NORMAL = 'normal'
    IMPORTANT = 'important'
    URGENT = 'urgent'


