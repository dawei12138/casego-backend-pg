#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：manager.py
@Author  ：david
@Date    ：2025-08-11 23:39 
"""
# utils/api_tools/executors/manager.py
from typing import List

from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult, CasesConfig
from utils.api_tools.executors.factory import ExecutorFactory
from utils.log_util import logger


class ExecutorManager:
    """前置/后置操作管理器"""

    def __init__(self):
        self.factory = ExecutorFactory()

    async def execute_setup_list(self, setup_list: List[SetupConfig], context: ExecutorContext) -> List[ExecutorResult]:
        """执行前置脚本列表"""
        logger.info(f"开始执行前置脚本，共{len(setup_list)}个")
        return await self._execute_list(setup_list, context, "setup_type")

    async def execute_teardown_list(self, teardown_list: List[TeardownConfig], context: ExecutorContext) -> List[
        ExecutorResult]:
        """执行后置脚本列表"""
        logger.info(f"开始执行后置脚本，共{len(teardown_list)}个")
        return await self._execute_list(teardown_list, context, "teardown_type")

    async def execute_apicase_list(self, api_list: List[CasesConfig], context: ExecutorContext) -> List[
        ExecutorResult]:
        """执行后置脚本列表"""
        logger.info(f"开始执行接口请求")
        return await self._execute_list(api_list, context, "APIExecutor")

    async def _execute_list(self, executor_list: List, context: ExecutorContext, list_type: str) -> List[
        ExecutorResult]:
        """通用执行列表方法"""
        results = []

        # 按sort_no排序执行
        sorted_list = sorted(executor_list, key=lambda x: x.sort_no)

        for config in sorted_list:
            if not config.is_run:
                # logger.debug(f"跳过执行 {list_type} 脚本: {config.name} (is_run=False)")
                continue

            try:
                # 获取执行器类型
                import time
                start_time = time.time()
                executor_type = getattr(config, f'{list_type}')

                # logger.info(f"执行 {list_type} 脚本: {config.name}, 类型: {executor_type}")

                # 创建执行器并执行
                executor = self.factory.create_executor(executor_type)
                time1 = time.time()
                # logger.warning(f"前置创建execcutor时间{time.time() - start_time}")

                result = await executor.execute(context, config)

                # logger.warning(f"前置单条执行耗时{time.time() - time1}")

                # # 更新上下文变量
                # if result.variables:
                #     context.variables.update(result.variables)
                #     logger.debug(f"更新变量: {result.variables}")

                # 记录执行结果
                if result.success:
                    logger.info(f"{list_type} 脚本执行成功: {config.name}: 结果：{result.model_dump()}")
                else:
                    logger.error(f"{list_type} 脚本执行失败: {config.name}, 错误: {result.error}")

                results.append(result)

            except Exception as e:
                logger.error(f"{list_type} 脚本执行异常: {config.name}, 异常: {str(e)}")
                error_result = ExecutorResult(
                    success=False,
                    error=f"执行器创建失败: {str(e)}"
                )
                results.append(error_result)

        logger.info(
            f"{list_type} 脚本执行完成，成功: {sum(1 for r in results if r.success)}, 失败: {sum(1 for r in results if not r.success)}")
        return results

    def execute_single(self, config, context: ExecutorContext) -> ExecutorResult:
        """执行单个脚本"""
        try:
            # 判断是setup还是teardown
            if hasattr(config, 'setup_type'):
                executor_type = config.setup_type
            else:
                executor_type = config.teardown_type

            executor = self.factory.create_executor(executor_type)
            result = executor.execute(context, config)

            # # 更新上下文变量
            # if result.variables:
            #     context.variables.update(result.variables)

            return result

        except Exception as e:
            return ExecutorResult(
                success=False,
                error=f"单个脚本执行失败: {str(e)}"
            )
