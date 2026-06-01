import enum


class DemoStatusEnum(str, enum.Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    DISABLED = 'disabled'
    TEST = 'test'
    TEST222 = "demo啊"


