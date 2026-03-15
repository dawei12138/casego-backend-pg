from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, List, Union, Any

from config.enums import Assertion_Method
from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import NodeTypeEnum


class TaskTypeEnum(str, Enum):
    """节点类型枚举"""
    WAIT = "wait"
    CUSTOMSCRIPT = "custom"
    PUBLICSCRIPT = "public_script"
    DB_OPERATION = "db_operation"
    APICASE = "api_case"
    API = "api"
    WEBCASE = "web_case"


class BreakConditionModel(BaseModel):
    """循环中断条件模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    expected_value: Optional[str] = Field(default=None, description='期望值')
    actual_value: Optional[str] = Field(default=None, description='实际值表达式')
    condition: Optional[Assertion_Method] = Field(default=Assertion_Method.EQUAL, description='比较条件操作符')


class ErrorHandlingStrategy(str, Enum):
    """错误处理策略枚举"""
    IGNORE = "ignore"  # 忽略错误，继续执行
    NEXT_ITERATION = "next_iteration"  # 跳到下一轮循环
    BREAK_LOOP = "break_loop"  # 结束循环
    STOP_RUNNING = "stop_running"  # 结束运行
    RETRY = "retry"  # 重试当前操作


class Task_config(BaseModel):
    """任务配置模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    task_type: Optional[TaskTypeEnum] = Field(default=None, description='任务类型')
    case_id: Optional[int] = Field(default=None, description='用例ID')
    api_id: Optional[int] = Field(default=None, description='接口ID')
    web_case_id: Optional[int] = Field(default=None, description='web自动化ID')
    db_operation_id: Optional[int] = Field(default=None, description='数据库连接ID')
    db_operation_script: Optional[str] = Field(default=None, description='数据库脚本')
    custom_script: Optional[str] = Field(default=None, description='自定义脚本')
    publicscript: Optional[str] = Field(default=None, description='公共脚本ID')

    wait_time: Optional[int] = Field(default=0, description='等待时间(毫秒)')


class NodeConfigModel(BaseModel):
    """节点配置信息模型 - 融合所有节点类型的配置"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    # group节点配置
    # name: Optional[str] = Field(default=None, description='分组名称')

    # task节点配置
    task_config: Optional[Task_config] = Field(default_factory=lambda: Task_config(), description="任务执行配置")
    # case_id: Optional[int] = Field(default=None, description='用例ID')
    # wait_time: Optional[int] = Field(default=0, description='等待时间(毫秒)')

    # if节点配置
    expected_value: Optional[Union[str, int, bool, float]] = Field(default=None, description='期望值')
    actual_value: Optional[str] = Field(default=None, description='实际值表达式')
    condition: Optional[Assertion_Method] = Field(default=Assertion_Method.EQUAL, description='比较条件操作符')
    else_node_id: Optional[int] = Field(default=None, description='else分支节点ID')

    # else节点配置
    bind_if_node_id: Optional[int] = Field(default=None, description='绑定的if节点ID')

    # for节点配置
    loop_count: Optional[int] = Field(default=1, description='循环次数')
    # 修复：使用 default_factory 而不是可变默认值
    break_condition: Optional[List[BreakConditionModel]] = Field(
        default_factory=lambda: [BreakConditionModel()],
        description='中断条件'
    )
    on_error: Optional[ErrorHandlingStrategy] = Field(
        default=ErrorHandlingStrategy.IGNORE,
        description='错误处理方式: ignore(忽略), next_iteration(跳到下一轮循环), break_loop(结束循环), stop_running(结束运行), retry(重试)'
    )

    # foreach节点配置
    loop_array: Optional[List[Union[str, int, float]]] = Field(default_factory=list, description='遍历数组')

    # 其他扩展配置
    extra_config: Optional[dict] = Field(default_factory=dict, description='其他配置信息')


class WorknodesModel(BaseModel):
    """执行器节点表对应pydantic模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    node_id: Optional[int] = Field(default=None, description='节点ID')
    workflow_id: Optional[int] = Field(default=None, description='所属执行器ID')
    parent_id: Optional[int] = Field(default=None, description='父节点ID')
    name: Optional[str] = Field(default="未命名", description='节点名称')
    type: Optional[NodeTypeEnum] = Field(default=None, description='节点类型')
    is_run: Optional[int] = Field(default=None, description='是否启用执行')
    children_ids: Optional[Union[List[dict], dict, List[int]]] = Field(
        default_factory=list,
        description='子结点列表'
    )
    config: Optional[NodeConfigModel] = Field(default_factory=lambda: NodeConfigModel(), description='节点配置信息')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')


class AddWorknodesModel(WorknodesModel):
    """新增执行器节点模型

    公共脚本、自定义脚本、数据库脚本、等待时间等直接通过config.taskConfig传入
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    # 从测试用例批量导入时使用
    case_ids: Optional[List[Union[str, int, float]]] = Field(default_factory=list, description='用例ID列表')

    # 添加HTTP请求/从curl导入时使用(需要创建type=3的用例)
    project_id: Optional[int] = Field(default=None, description='项目ID')
    curl_command: Optional[str] = Field(default=None, description='cURL命令字符串')

    # 排序定位参数：指定新节点插入到哪个节点之后
    after_node_id: Optional[int] = Field(default=None, description='在此节点之后插入，为空则插入到同级末尾')


class WorknodesModelWithChildren(WorknodesModel):
    """带子节点列表的执行器节点模型"""

    # 如果需要覆盖父类的配置，可以重新定义
    # model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    children: Optional[List['WorknodesModelWithChildren']] = Field(
        default_factory=list,
        description='子节点列表（嵌套结构）'
    )


class WorknodesQueryModel(WorknodesModel):
    """执行器节点不分页查询模型"""
    pass


class WorknodesSortModel(BaseModel):
    """工作节点排序模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    sorted_nodes: List[WorknodesModel] = Field(
        default_factory=list,
        description='排序后的节点列表，按列表顺序表示排序结果'
    )


@as_query
class WorknodesPageQueryModel(WorknodesQueryModel):
    """执行器节点分页查询模型"""
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteWorknodesModel(BaseModel):
    """删除执行器节点模型"""
    model_config = ConfigDict(alias_generator=to_camel)

    node_ids: str = Field(description='需要删除的节点ID')


class CopyWorknodesModel(BaseModel):
    """复制执行器节点模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    node_id: int = Field(description='需要复制的节点ID')
    target_parent_id: Optional[int] = Field(default=None, description='目标父节点ID，为空则复制到同级')
