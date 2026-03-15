import asyncio
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, AsyncGenerator, Union
from abc import ABC, abstractmethod
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ConfigDict
import logging

from pydantic.alias_generators import to_camel

from config.enums import Assertion_Method
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataQueryModel
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import NodeTypeEnum
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import WorknodesModelWithChildren, \
    ErrorHandlingStrategy, NodeConfigModel
from module_admin.api_workflow.workflow.entity.vo.workflow_vo import WorkflowTreeModel, ExecutionConfigModel
from utils.api_tools.executors.models import ExecutorContext
from utils.api_tools.regular_control import advanced_template_parser
from utils.api_workflow_tools.api_task_exectors import TaskExecutorManager
from utils.api_workflow_tools.models import StreamingExecutionContext, StreamEvent, StreamEventType
from utils.log_util import logger


class StreamingNodeExecutor(ABC):
    """流式节点执行器基类"""

    def __init__(self, workflow_executor: 'StreamingWorkflowExecutor'):
        self.workflow_executor = workflow_executor
        self.logger = logger

    async def execute_with_stream(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:
        """执行节点并流式返回结果"""


        start_time = time.time()

        try:
            # 检查节点是否启用
            if node.is_run != 1:
                context.increment_skipped()
                return

            # 执行具体节点逻辑
            async for event in self.execute_node_logic(node, context):
                yield event

            # 更新完成计数
            context.increment_completed()

        except Exception as e:
            execution_time = time.time() - start_time
            context.increment_failed()

            error_msg = f"节点执行失败: {str(e)}"
            self.logger.error(f"节点 {node.node_id} 执行失败: {e}")

            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                node_id=node.node_id,
                message=error_msg,
                data={
                    "executionTime": execution_time,
                    "error": str(e),
                    "errorType": type(e).__name__
                }
            )

            # 根据错误处理策略决定是否继续执行
            if not self.should_continue_on_error(e, node):
                context.should_stop = True

    @abstractmethod
    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:
        """执行节点具体逻辑（子类实现）"""
        pass

    def should_continue_on_error(self, error: Exception, node: WorknodesModelWithChildren) -> bool:
        """发生错误时是否继续执行"""
        # 根据节点配置的错误处理策略决定
        if node.config and hasattr(node.config, 'on_error'):
            strategy = node.config.on_error
            if strategy == ErrorHandlingStrategy.STOP_RUNNING:
                return False
            elif strategy == ErrorHandlingStrategy.IGNORE:
                return True

        # 默认继续执行
        return True

    def compare_values(self, actual_value: Any, expected_value: Any, compare_type: str) -> bool:
        """优化的值比较函数"""

        # 空值判断
        if compare_type in ["is_null", "IS_NULL"]:
            return actual_value is None or actual_value == ""

        if compare_type in ["is_not_null", "IS_NOT_NULL"]:
            return actual_value is not None and actual_value != ""

        if compare_type in ["exist", "EXIST"]:
            return actual_value is not None

        if compare_type in ["not_exist", "NOT_EXIST"]:
            return actual_value is None

        if actual_value is None:
            return False

        # 先转换为字符串并去除空格
        actual_str = str(actual_value).strip()
        expected_str = str(expected_value).strip()

        # 等于/不等于比较 - 优先尝试数值比较
        if compare_type in ["=", "==", "EQUAL"]:
            # 先尝试数值比较
            try:
                actual_num = float(actual_str)
                expected_num = float(expected_str)
                return actual_num == expected_num
            except (ValueError, TypeError):
                # 数值转换失败，使用字符串比较
                return actual_str == expected_str

        if compare_type in ["!=", "NOT_EQUAL"]:
            # 先尝试数值比较
            try:
                actual_num = float(actual_str)
                expected_num = float(expected_str)
                return actual_num != expected_num
            except (ValueError, TypeError):
                # 数值转换失败，使用字符串比较
                return actual_str != expected_str

        # 数值比较
        if compare_type in [">", ">=", "<", "<=", "GREATER_THAN", "LESS_THAN", "GREATER_EQUAL", "LESS_EQUAL"]:
            try:
                actual_num = float(actual_str)
                expected_num = float(expected_str)
                if compare_type in [">", "GREATER_THAN"]:
                    return actual_num > expected_num
                elif compare_type in [">=", "GREATER_EQUAL"]:
                    return actual_num >= expected_num
                elif compare_type in ["<", "LESS_THAN"]:
                    return actual_num < expected_num
                elif compare_type in ["<=", "LESS_EQUAL"]:
                    return actual_num <= expected_num
            except (ValueError, TypeError):
                return False

        # 字符串操作
        if compare_type in ["contain", "CONTAINS"]:
            return expected_str in actual_str

        if compare_type in ["not_contain", "NOT_CONTAINS"]:
            return expected_str not in actual_str

        # 正则匹配
        if compare_type == "REGULAR_TYPE":
            try:
                return bool(re.search(expected_str, actual_str))
            except re.error:
                return False

        # 集合操作
        if compare_type in ["belong_to_set", "BELONG_TO_SET"]:
            if isinstance(expected_value, (list, tuple, set)):
                return actual_value in expected_value
            return False

        if compare_type in ["not_belong_to_set", "NOT_BELONG_TO_SET"]:
            if isinstance(expected_value, (list, tuple, set)):
                return actual_value not in expected_value
            return True

        return False

    async def resolve_expression_with_parser(self, expression: Any, context: StreamingExecutionContext) -> Any:
        """使用高级模板解析器解析表达式"""
        if not expression:
            return expression

        try:
            # 创建查询对象
            query_obj = Cache_dataQueryModel(
                user_id=context.executor_context.user_id,
                environment_id=context.executor_context.env_id
            )

            # 使用高级模板解析器解析表达式
            resolved_value = await advanced_template_parser(
                template=expression,
                redis=context.executor_context.redis_obj,
                query_object=query_obj,
                variables_dict=context.executor_context.parameterization
            )

            # 尝试转换为适当的类型
            # return self._convert_to_appropriate_type(resolved_value)
            return resolved_value

        except Exception as e:
            self.logger.error(f"表达式解析失败: {e}")
            return expression

    async def evaluate_condition(self, expected: Any, actual: Any, condition: Union[Assertion_Method, str],
                                 context: StreamingExecutionContext) -> bool:
        """优化的条件评估函数"""
        try:
            # 解析表达式中的变量
            resolved_actual = await self.resolve_expression_with_parser(actual, context)
            resolved_expected = await self.resolve_expression_with_parser(expected, context)

            # 获取比较类型字符串
            if isinstance(condition, Assertion_Method):
                # 从原始枚举映射到扩展枚举
                condition_mapping = {
                    Assertion_Method.EQUAL: "=",
                    Assertion_Method.NOT_EQUAL: "!=",
                    Assertion_Method.BIG_THAN: ">",
                    Assertion_Method.LESS_THAN: "<",
                    Assertion_Method.BIG_THAN_OR_EQUAL: ">=",
                    Assertion_Method.LESS_THAN_OR_EQUAL: "<=",
                    Assertion_Method.CONTAIN: "contain",
                    Assertion_Method.NOT_CONTAIN: "not_contain",
                }
                compare_type = condition_mapping.get(condition, "=")
            else:
                compare_type = str(condition)

            # 使用优化的比较函数
            result = self.compare_values(resolved_actual, resolved_expected, compare_type)

            self.logger.info(
                f"条件评估: 实际值='{resolved_actual}' {compare_type} 期望值='{resolved_expected}' => {result}")

            return result

        except Exception as e:
            self.logger.error(f"条件评估失败: {e}")
            return False

    async def execute_children_stream(
            self,
            children: List[WorknodesModelWithChildren],
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:
        """流式执行子节点"""
        for child in children:
            if context.should_stop:
                break

            async for event in self.workflow_executor.execute_node_stream(child, context):
                yield event

                # 检查是否需要发送心跳
                if context.should_send_heartbeat():
                    yield StreamEvent(
                        event_type=StreamEventType.LOG,
                        workflow_id=context.workflow_id,
                        message="保持连接",
                        progress=context.get_progress(),
                        data=context.get_runtime_stats()
                    )
                    context.update_heartbeat()


class StreamingTaskNodeExecutor(StreamingNodeExecutor):
    """流式Task节点执行器"""

    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:

        config = node.config
        executor_ctx = context.executor_context

        # 发送任务开始日志
        # yield StreamEvent(
        #     event_type=StreamEventType.LOG,
        #     workflow_id=context.workflow_id,
        #     node_id=node.node_id,
        #     message=f"执行任务 {config.task_config.task_type.value}: user_id: {executor_ctx.user_id}, env_id: {executor_ctx.env_id}"
        # )

        try:
            if config:
                # # 执行前的准备工作
                # yield StreamEvent(
                #     event_type=StreamEventType.LOG,
                #     workflow_id=context.workflow_id,
                #     node_id=node.node_id,
                #     message=f"准备执行任务，环境ID: {executor_ctx.env_id}, 用户ID: {executor_ctx.user_id}"
                # )

                # 实际的任务执行逻辑
                task_result = await self._execute_actual_task(config, executor_ctx, context, node)

                # 保存任务结果到上下文变量中
                context.set_variable(f"task_result_{node.node_id}", task_result)
                context.executor_context.response = task_result  # 保存最后的响应

                # 判断是否是 API/Case 类型的任务（有 response 属性）
                if hasattr(task_result, 'response') and task_result.response:
                    # API/Case 类型任务，使用 CASE_RESULT 事件类型
                    if hasattr(task_result.response,'case_name'):
                        # case名称修改为node节点名称
                        task_result.response.case_name = node.name

                    message = f"{node.name} 成功" if task_result.response.is_success else f"{node.name}失败"
                    yield StreamEvent(
                        event_type=StreamEventType.CASE_RESULT,
                        workflow_id=context.workflow_id,
                        node_id=node.node_id,
                        message=message,
                        data=json.loads(task_result.model_dump_json(by_alias=True)),
                        case_id=config.task_config.api_id,
                        # execution_time=task_result.response.execution_time,
                        method=task_result.response.request_method,
                        path=task_result.response.request_url,
                        # name=task_result.response.case_name,
                        name=node.name,
                        is_success=task_result.response.is_success,
                        response_status_code=task_result.response.response_status_code,
                        response_time=task_result.response.response_time,
                        assertion_success=task_result.assersion_result.success,
                    )
                else:
                    # 其他任务类型（WAIT、数据库、脚本等），使用 LOG 事件类型
                    message = task_result.message if hasattr(task_result, 'message') else "任务执行完成"
                    is_success = task_result.success if hasattr(task_result, 'success') else True
                    yield StreamEvent(
                        event_type=StreamEventType.LOG,
                        workflow_id=context.workflow_id,
                        node_id=node.node_id,
                        message=f"{node.name or '任务'}: {message}",
                        is_success=is_success,
                        data=json.loads(task_result.model_dump_json()) if hasattr(task_result, 'model_dump_json') else None
                    )

        except Exception as e:
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                node_id=node.node_id,
                message=f"任务执行失败: {str(e)}"
            )
            raise

    async def _execute_actual_task(self, config: NodeConfigModel, executor_ctx: ExecutorContext,
                                   streaming_ctx: StreamingExecutionContext, node: WorknodesModelWithChildren) -> Dict[
        str, Any]:
        """执行具体任务的逻辑"""
        manager = TaskExecutorManager(config, streaming_ctx, node, executor_ctx)
        result = await manager.execute_task()

        # print(result)
        # 模拟执行时间
        # 示例：检查环境配置
        if executor_ctx.env_config:
            # 使用环境配置执行任务
            pass

        # 示例：使用数据库连接
        if executor_ctx.mysql_obj:
            # 执行数据库查询
            pass

        # 示例：使用参数化数据
        param_data = executor_ctx.parameterization

        # 返回模拟的任务执行结果
        return result


class StreamingIfNodeExecutor(StreamingNodeExecutor):
    """流式If节点执行器"""

    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:

        config = node.config

        if not config:
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                node_id=node.node_id,
                message="If节点缺少配置信息"
            )
            return

        # 评估条件
        condition_result = await self.evaluate_condition(
            config.expected_value,
            config.actual_value,
            config.condition or Assertion_Method.EQUAL,
            context
        )

        yield StreamEvent(
            event_type=StreamEventType.LOG,
            workflow_id=context.workflow_id,
            node_id=node.node_id,
            message=f"条件判断结果: {condition_result}",
            data={
                "expected": config.expected_value,
                "actual": config.actual_value,
                "condition": config.condition.value if config.condition else "=",
                "result": condition_result
            }
        )

        if condition_result:
            # 执行if分支（排除else节点）
            if_children = [child for child in (node.children or []) if child.type != NodeTypeEnum.ELSE]
            if if_children:
                # yield StreamEvent(
                #     event_type=StreamEventType.LOG,
                #     workflow_id=context.workflow_id,
                #     node_id=node.node_id,
                #     message=f"执行IF分支，包含 {len(if_children)} 个子节点"
                # )
                logger.info("执行IF分支，包含 {len(if_children)} 个子节点")
                async for event in self.execute_children_stream(if_children, context):
                    yield event
        else:
            # 执行else分支
            else_node = next((child for child in (node.children or []) if child.type == NodeTypeEnum.ELSE), None)
            if else_node:
                yield StreamEvent(
                    event_type=StreamEventType.LOG,
                    workflow_id=context.workflow_id,
                    node_id=node.node_id,
                    message="执行ELSE分支"
                )
                async for event in self.workflow_executor.execute_node_stream(else_node, context):
                    yield event
            else:
                yield StreamEvent(
                    event_type=StreamEventType.LOG,
                    workflow_id=context.workflow_id,
                    node_id=node.node_id,
                    message="条件为假，无ELSE分支，跳过"
                )


class StreamingElseNodeExecutor(StreamingNodeExecutor):
    """流式Else节点执行器"""

    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:

        # yield StreamEvent(
        #     event_type=StreamEventType.LOG,
        #     workflow_id=context.workflow_id,
        #     node_id=node.node_id,
        #     message="执行Else节点内容"
        # )

        # 执行else节点的所有子节点
        if node.children:
            async for event in self.execute_children_stream(node.children, context):
                yield event


class StreamingForNodeExecutor(StreamingNodeExecutor):
    """流式For循环节点执行器"""

    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:

        config = node.config
        if not config:
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                node_id=node.node_id,
                message="For节点缺少配置信息"
            )
            return

        loop_count = config.loop_count or 1

        # 发送循环开始事件
        yield StreamEvent(
            event_type=StreamEventType.LOG,
            workflow_id=context.workflow_id,
            node_id=node.node_id,
            message=f"开始For循环，总计 {loop_count} 次",
            data={"loopType": "for", "totalCount": loop_count}
        )

        # 循环信息压栈
        loop_info = {
            "type": "for",
            "nodeId": node.node_id,
            "currentIndex": 0,
            "totalCount": loop_count
        }
        context.loop_stack.append(loop_info)

        try:
            for i in range(loop_count):
                if context.should_stop or context.should_break:
                    yield StreamEvent(
                        event_type=StreamEventType.LOG,
                        workflow_id=context.workflow_id,
                        node_id=node.node_id,
                        message=f"循环提前结束于第 {i + 1} 次"
                    )
                    break

                # 更新循环信息
                context.loop_stack[-1]["currentIndex"] = i
                context.set_variable("loop_index", i)
                context.set_variable("loop_count", loop_count)

                # 发送循环迭代事件
                yield StreamEvent(
                    event_type=StreamEventType.LOG,
                    workflow_id=context.workflow_id,
                    node_id=node.node_id,
                    message=f"第 {i + 1}/{loop_count} 次循环",
                    data={"currentIndex": i, "loopItem": None, "totalCount": loop_count}
                )

                try:
                    # 执行循环体
                    if node.children:
                        async for event in self.execute_children_stream(node.children, context):
                            yield event

                    # 检查中断条件
                    if await self._check_break_conditions(config.break_condition, context):
                        yield StreamEvent(
                            event_type=StreamEventType.LOG,
                            workflow_id=context.workflow_id,
                            node_id=node.node_id,
                            message=f"满足中断条件，循环在第 {i + 1} 次结束"
                        )
                        break

                except Exception as e:
                    # 根据错误处理策略处理
                    strategy = config.on_error or ErrorHandlingStrategy.IGNORE
                    yield StreamEvent(
                        event_type=StreamEventType.ERROR,
                        workflow_id=context.workflow_id,
                        node_id=node.node_id,
                        message=f"循环第 {i + 1} 次执行出错: {str(e)}，策略: {strategy.value}"
                    )

                    if strategy == ErrorHandlingStrategy.BREAK_LOOP:
                        context.should_break = True
                        break
                    elif strategy == ErrorHandlingStrategy.STOP_RUNNING:
                        context.should_stop = True
                        break
                    elif strategy == ErrorHandlingStrategy.NEXT_ITERATION:
                        continue
                    # IGNORE 或 RETRY 策略继续执行

                # 重置循环控制标志
                context.should_continue = False

        finally:
            # 弹出循环信息
            context.loop_stack.pop()
            context.should_break = False

        # 发送循环结束事件
        # yield StreamEvent(
        #     event_type=StreamEventType.LOOP_END,
        #     workflow_id=context.workflow_id,
        #     node_id=node.node_id,
        #     message=f"For循环执行完成"
        # )

    async def _check_break_conditions(self, conditions: List, context: StreamingExecutionContext) -> bool:
        """检查中断条件"""
        if not conditions:
            return False

        for condition in conditions:
            if hasattr(condition, 'expected_value') and hasattr(condition, 'actual_value'):
                if await self.evaluate_condition(
                        condition.expected_value,
                        condition.actual_value,
                        condition.condition or Assertion_Method.EQUAL,
                        context
                ):
                    return True

        return False


class StreamingForeachNodeExecutor(StreamingNodeExecutor):
    """流式Foreach循环节点执行器"""

    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:

        config = node.config
        if not config:
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                node_id=node.node_id,
                message="Foreach节点缺少配置信息"
            )
            return

        loop_array = config.loop_array or []

        # 发送循环开始事件
        yield StreamEvent(
            event_type=StreamEventType.LOG,
            workflow_id=context.workflow_id,
            node_id=node.node_id,
            message=f"开始Foreach循环，数组长度: {len(loop_array)}",
            data={"loopType": "foreach", "totalCount": len(loop_array), "array": loop_array}
        )

        # 循环信息压栈
        loop_info = {
            "type": "foreach",
            "nodeId": node.node_id,
            "currentIndex": 0,
            "array": loop_array
        }
        context.loop_stack.append(loop_info)

        try:
            for index, item in enumerate(loop_array):
                if context.should_stop or context.should_break:
                    break

                # 更新循环信息
                context.loop_stack[-1]["currentIndex"] = index
                context.set_variable("loop_index", index)
                context.set_variable("loop_item", item)

                # 发送循环迭代事件
                yield StreamEvent(
                    event_type=StreamEventType.LOG,
                    workflow_id=context.workflow_id,
                    node_id=node.node_id,
                    message=f"Foreach循环第 {index + 1}/{len(loop_array)} 次迭代",
                    data={"currentIndex": index, "loopItem": item, "totalCount": len(loop_array)}
                )

                try:
                    # 执行循环体
                    if node.children:
                        async for event in self.execute_children_stream(node.children, context):
                            yield event

                except Exception as e:
                    strategy = config.on_error or ErrorHandlingStrategy.IGNORE
                    yield StreamEvent(
                        event_type=StreamEventType.ERROR,
                        workflow_id=context.workflow_id,
                        node_id=node.node_id,
                        message=f"Foreach循环第 {index + 1} 次执行出错: {str(e)}"
                    )

                    if strategy == ErrorHandlingStrategy.BREAK_LOOP:
                        break
                    elif strategy == ErrorHandlingStrategy.STOP_RUNNING:
                        context.should_stop = True
                        break

                context.should_continue = False

        finally:
            context.loop_stack.pop()
            context.should_break = False

        # # 发送循环结束事件
        # yield StreamEvent(
        #     event_type=StreamEventType.LOOP_END,
        #     workflow_id=context.workflow_id,
        #     node_id=node.node_id,
        #     message=f"Foreach循环执行完成"
        # )


class StreamingGroupNodeExecutor(StreamingNodeExecutor):
    """流式Group节点执行器"""

    async def execute_node_logic(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:

        # yield StreamEvent(
        #     event_type=StreamEventType.LOG,
        #     workflow_id=context.workflow_id,
        #     node_id=node.node_id,
        #     message=
        # )
        logger.info(f"开始执行Group节点: {node.name or 'Group'}")
        # Group节点只是一个逻辑分组，直接执行所有子节点
        if node.children:
            # yield StreamEvent(
            #     event_type=StreamEventType.LOG,
            #     workflow_id=context.workflow_id,
            #     node_id=node.node_id,
            #     message=f"Group包含 {len(node.children)} 个子节点"
            # )
            async for event in self.execute_children_stream(node.children, context):
                yield event


class StreamingWorkflowExecutor:
    """流式工作流执行器"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        # 注册流式节点执行器
        self.node_executors = {
            NodeTypeEnum.TASK: StreamingTaskNodeExecutor(self),
            NodeTypeEnum.IF: StreamingIfNodeExecutor(self),
            NodeTypeEnum.ELSE: StreamingElseNodeExecutor(self),
            NodeTypeEnum.FOR: StreamingForNodeExecutor(self),
            NodeTypeEnum.FOREACH: StreamingForeachNodeExecutor(self),
            NodeTypeEnum.GROUP: StreamingGroupNodeExecutor(self),
        }

    def count_total_nodes(self, worknodes: Union[List[WorknodesModelWithChildren], WorknodesModelWithChildren]) -> int:
        """递归计算总节点数（支持Pydantic模型）"""
        total = 0

        # 处理单个节点
        if isinstance(worknodes, WorknodesModelWithChildren):
            total += 1
            if worknodes.children:
                total += self.count_total_nodes(worknodes.children)

        # 处理节点列表
        elif isinstance(worknodes, list):
            for node in worknodes:
                total += 1  # 当前节点
                if hasattr(node, 'children') and node.children:
                    total += self.count_total_nodes(node.children)

        return total

    async def execute_workflow_stream(
            self,
            workflow: WorkflowTreeModel,
            executor_context: ExecutorContext,
            initial_context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        流式执行工作流（接收Pydantic模型和执行器上下文）
        :param workflow:
        :param executor_context:
        :param initial_context:
        :return:
        """

        context = StreamingExecutionContext(executor_context=executor_context)
        context.workflow_id = workflow.workflow_id

        # 初始化上下文变量
        if initial_context:
            context.executor_context.variables.update(initial_context)

        # 如果工作流配置中有参数化数据，添加到上下文中
        if workflow.execution_config:
            if isinstance(workflow.execution_config, ExecutionConfigModel):
                context.execution_config = workflow.execution_config
                # 如果有参数化数据，解析并添加到上下文
                if workflow.execution_config.parameterization_data:
                    # TODO: 解析参数化数据并添加到 executor_context.parameterization11
                    pass
            elif isinstance(workflow.execution_config, dict):
                context.execution_config = ExecutionConfigModel(**workflow.execution_config)

        # 处理 worknodes
        worknodes = []
        if workflow.worknodes:
            if isinstance(workflow.worknodes, list):
                worknodes = workflow.worknodes
            elif isinstance(workflow.worknodes, WorknodesModelWithChildren):
                worknodes = [workflow.worknodes]

        # 计算总节点数
        context.total_nodes = self.count_total_nodes(worknodes)

        # 发送工作流开始事件
        yield StreamEvent(
            event_type=StreamEventType.LOG,
            workflow_id=context.workflow_id,
            message=f"开始执行工作流: {workflow.name}",
            data={
                "workflowId": workflow.workflow_id,
                "workflowName": workflow.name,
                "totalNodes": context.total_nodes,
                "executionConfig": context.execution_config.model_dump() if context.execution_config else None
            }
        )

        # 发送执行配置信息
        if context.execution_config:
            pass
            # yield StreamEvent(
            #     event_type=StreamEventType.CONFIG_INFO,
            #     workflow_id=context.workflow_id,
            #     message="工作流执行配置",
            #     data=context.execution_config.model_dump()
            # )

        try:
            # 处理多次循环执行（根据execution_config.loop_count）
            loop_count = 1
            if context.execution_config and context.execution_config.loop_count:
                loop_count = context.execution_config.loop_count

            for workflow_loop in range(loop_count):
                if context.should_stop:
                    break

                if loop_count > 1:
                    yield StreamEvent(
                        event_type=StreamEventType.LOG,
                        workflow_id=context.workflow_id,
                        message=f"工作流第 {workflow_loop + 1}/{loop_count} 次循环"
                    )
                    context.set_variable("workflow_loop_index", workflow_loop)

                # 执行所有根节点
                for node in worknodes:
                    if context.should_stop:
                        break

                    # 流式执行节点
                    async for event in self.execute_node_stream(node, context):
                        yield event

            # 发送工作流完成事件
            execution_time = (datetime.now() - context.start_time).total_seconds()
            final_stats = context.get_runtime_stats()

            yield StreamEvent(
                event_type=StreamEventType.LOG,
                workflow_id=context.workflow_id,
                message="工作流执行完成",
                progress=100.0,
                data={
                    "totalExecutionTime": execution_time,
                    "finalStats": final_stats
                }
            )

        except Exception as e:
            self.logger.error(f"工作流执行失败: {e}")
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                message=f"工作流执行失败: {str(e)}",
                data={
                    "errorType": type(e).__name__,
                    "stats": context.get_runtime_stats()
                }
            )

    async def execute_node_stream(
            self,
            node: WorknodesModelWithChildren,
            context: StreamingExecutionContext
    ) -> AsyncGenerator[StreamEvent, None]:
        """流式执行单个节点"""

        # 获取对应的节点执行器
        executor = self.node_executors.get(node.type)
        if not executor:
            error_msg = f"不支持的节点类型: {node.type}"
            self.logger.error(error_msg)
            yield StreamEvent(
                event_type=StreamEventType.ERROR,
                workflow_id=context.workflow_id,
                node_id=node.node_id,
                message=error_msg
            )
            return

        # 流式执行节点
        async for event in executor.execute_with_stream(node, context):
            yield event
