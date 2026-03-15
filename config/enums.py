from enum import Enum


class Module_type(Enum):
    api_submodule = "1"
    api_suite = "2"
    ui_submodule = "3"
    NULL = None


class Request_method(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'
    PATCH = 'PATCH'
    TRACE = 'TRACE'
    CONNECT = 'CONNECT'
    COPY = 'COPY'
    LINK = 'LINK'
    UNLINK = 'UNLINK'
    PURGE = 'PURGE'
    LOCK = 'LOCK'
    UNLOCK = 'UNLOCK'
    MKCOL = 'MKCOL'
    MOVE = 'MOVE'
    PROPFIND = 'PROPFIND'
    REPORT = 'REPORT'
    VIEW = 'VIEW'

    def __str__(self):
        return self.value


class Dependentmethod(Enum):
    RESPONSE = 'response'
    REQUEST = 'request'
    HEADERS = 'headers'

    def __str__(self):
        return self.value


class DataTypeEnum(Enum):
    STRING = 'string'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    NUMBER = 'number'
    ARRAY = 'array'
    FILE = 'file'


class DependentType(Enum):
    SETUP = 'setup'
    TEARDOWN = 'teardown'

    def __str__(self):
        return self.value


class Assert_Type(Enum):
    Response_Text = 'response_text'
    Response_JSON = 'response_json'
    Response_XML = 'response_xml'
    Response_Header = 'response_header'
    Response_Cookie = 'response_cookie'
    Response_Status = 'response_status'
    Environment_Cache = 'environment_cache'

    def __str__(self):
        return self.value


class Assertion_Method(str, Enum):
    # json 序列化友好
    EQUAL = "="
    NOT_EQUAL = "!="
    EXIST = "exist"
    NOT_EXIST = "not_exist"
    BIG_THAN = ">"
    BIG_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    REGULAR_TYPE = "REGULAR_TYPE"
    CONTAIN = "contain"
    NOT_CONTAIN = "not_contain"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    BELONG_TO_SET = "belong_to_set"
    NOT_BELONG_TO_SET = "not_belong_to_set"

    def __str__(self):
        return self.value


class TeardownType(Enum):
    EXTRACT_VARIABLE = 'EXTRACT_VARIABLE'
    DB_CONNECTION = 'DB_CONNECTION'
    PYTHON_SCRIPT = 'PYTHON_SCRIPT'
    JS_SCRIPT = 'JS_SCRIPT'
    WAIT_TIME = 'WAIT_TIME'
    NONE = None

    def __str__(self):
        return self.value


class Teardown_extract_variable_method(Enum):
    Response_Text = 'response_text'
    Response_JSON = 'response_json'
    Response_XML = 'response_xml'
    Response_Header = 'response_header'
    Response_Cookie = 'response_cookie'

    def __str__(self):
        return self.value


class ScriptType:
    PYTHON = "PYTHON"
    JavaScript = "JavaScript"
    DB = "DB"


class SetupType(Enum):
    DB_CONNECTION = 'DB_CONNECTION'
    PYTHON_SCRIPT = 'PYTHON_SCRIPT'
    JS_SCRIPT = 'JS_SCRIPT'
    WAIT_TIME = 'WAIT_TIME'

    def __str__(self):
        return self.value


class Request_Type(Enum):
    NONE = "NONE"
    Form_Data = "Form_Data"
    x_www_form_urlencoded = "x_www_form_urlencoded"
    JSON = "JSON"
    XML = "XML"
    Raw = "Raw"
    Binary = "Binary"

    def __str__(self):
        return self.value


class BusinessType(Enum):
    """
    业务操作类型

    OTHER: 其它
    INSERT: 新增
    UPDATE: 修改
    DELETE: 删除
    GRANT: 授权
    EXPORT: 导出
    IMPORT: 导入
    FORCE: 强退
    GENCODE: 生成代码
    CLEAN: 清空数据
    """

    OTHER = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    GRANT = 4
    EXPORT = 5
    IMPORT = 6
    FORCE = 7
    GENCODE = 8
    CLEAN = 9


class RedisInitKeyConfig(Enum):
    """
    系统内置Redis键名
    """

    @property
    def key(self):
        return self.value.get('key')

    @property
    def remark(self):
        return self.value.get('remark')

    ACCESS_TOKEN = {'key': 'access_token', 'remark': '登录令牌信息'}
    SYS_DICT = {'key': 'sys_dict', 'remark': '数据字典'}
    SYS_CONFIG = {'key': 'sys_config', 'remark': '配置信息'}
    CAPTCHA_CODES = {'key': 'captcha_codes', 'remark': '图片验证码'}
    ACCOUNT_LOCK = {'key': 'account_lock', 'remark': '用户锁定'}
    PASSWORD_ERROR_COUNT = {'key': 'password_error_count', 'remark': '密码错误次数'}
    SMS_CODE = {'key': 'sms_code', 'remark': '短信验证码'}
    TASKLOCK = {'key': 'scheduler', 'remark': '任务调度锁'}
    ENVCACHE = {'key': 'environment_cache:user', 'remark': '环境缓存'}


class WebSocketMessageType(str, Enum):
    """
    WebSocket 消息类型枚举
    """
    # 连接相关
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'

    # 工作流相关
    WORKFLOW_START = 'workflow_start'
    WORKFLOW_COMPLETE = 'workflow_complete'
    WORKFLOW_FAILED = 'workflow_failed'
    WORKFLOW_PROGRESS = 'workflow_progress'

    # 节点执行相关
    NODE_START = 'node_start'
    NODE_COMPLETE = 'node_complete'
    NODE_FAILED = 'node_failed'

    # 定时任务相关
    TASK_START = 'task_start'
    TASK_COMPLETE = 'task_complete'
    TASK_FAILED = 'task_failed'

    # 测试用例相关
    TESTCASE_START = 'testcase_start'
    TESTCASE_COMPLETE = 'testcase_complete'
    TESTCASE_FAILED = 'testcase_failed'

    # 系统相关
    SYSTEM_NOTICE = 'system_notice'
    SYSTEM_WARNING = 'system_warning'
    SYSTEM_ERROR = 'system_error'

    # 工作区文件相关
    WORKSPACE_CHANGED = 'workspace_changed'


class WebSocketCloseCode(Enum):
    """
    WebSocket 关闭代码枚举
    """
    NORMAL = 1000           # 正常关闭
    AUTH_FAILED = 4001      # 认证失败
    TOKEN_EXPIRED = 4002    # Token 已过期
    PARAM_ERROR = 4003      # 参数错误
    SERVER_ERROR = 4004     # 服务器错误


class NotificationType(str, Enum):
    """通知类型枚举"""
    SUCCESS = "success"  # 成功通知
    ERROR = "error"  # 失败通知
    ALERT = "alert"  # 告警通知
