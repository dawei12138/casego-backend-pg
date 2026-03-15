#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import asyncio
import multiprocessing as mp
from datetime import datetime
from typing import List, Dict, Any
import traceback
import warnings

# 忽略asyncio警告
warnings.filterwarnings('ignore', category=RuntimeWarning, module='asyncio')

from config.get_db import get_db
from config.get_httpclient import get_http_client
from config.get_redis import RedisUtil
from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsConfig
from module_admin.api_testing.api_environments.service.environments_service import EnvironmentsService
from module_admin.api_workflow.api_param_item.dao.api_param_item_dao import Api_param_itemDao
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemPageQueryModel
from module_admin.api_workflow.workflow.service.workflow_service import WorkflowService
from utils.api_tools.executors.models import ExecutorContext
from utils.api_workflow_tools.api_workflows_exectors import StreamingWorkflowExecutor
from utils.log_util import logger


def execute_param_item_in_process(
        workflow_id: int,
        param_item_data: Dict[str, Any],
        env_id: int,
        process_id: int
) -> Dict[str, Any]:
    """
    在独立进程中执行单个数据集 - 修复版本

    关键：每个进程有独立的内存空间和事件循环
    修复：正确清理异步生成器，避免 Task pending 错误

    Args:
        workflow_id: 工作流ID
        param_item_data: 参数化数据（字典形式）
        env_id: 环境ID
        process_id: 进程编号
    """
    loop = None
    try:
        # 每个进程需要创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # 在事件循环中运行异步任务
        result = loop.run_until_complete(
            _async_execute_param_item(workflow_id, param_item_data, env_id, process_id)
        )

        return result

    except Exception as e:
        print(f"[进程 {process_id}] 执行失败: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "process_id": process_id,
            "group_name": param_item_data.get("group_name", "Unknown"),
            "error": str(e),
            "error_type": type(e).__name__
        }
    finally:
        # 🔧 修复：正确清理事件循环，避免 Task pending 错误
        if loop:
            try:
                # 1. 等待所有pending tasks完成(最多1秒)
                pending = asyncio.all_tasks(loop)
                if pending:
                    loop.run_until_complete(asyncio.wait(pending, timeout=1.0))

                # 2. 取消所有剩余任务
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()

                # 3. 再次运行以处理取消
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))

                # 4. 关闭异步生成器 (关键!)
                loop.run_until_complete(loop.shutdown_asyncgens())

                # 5. 关闭默认executor (Python 3.9+)
                try:
                    loop.run_until_complete(loop.shutdown_default_executor())
                except AttributeError:
                    pass

                # 6. 最后关闭循环
                loop.close()

            except Exception as e:
                logger.debug(f"清理事件循环失败(忽略): {e}")


async def _async_execute_param_item(
        workflow_id: int,
        param_item_data: Dict[str, Any],
        env_id: int,
        process_id: int
) -> Dict[str, Any]:
    """
    异步执行单个数据集 - 修复版本

    修复：使用generator的aclose()管理资源，避免资源泄漏
    """
    query_db = None
    session = None
    redis = None
    db_gen = None
    http_gen = None

    try:
        # 获取异步生成器
        db_gen = get_db()
        query_db = await db_gen.__anext__()

        http_gen = get_http_client()
        session = await http_gen.__anext__()

        redis = await RedisUtil.create_redis_pool()

        group_name = param_item_data.get("group_name", "Unknown")
        item_data = param_item_data.get("item", {})

        print(f"[进程 {process_id}] 开始执行数据集: {group_name}")

        # 获取环境配置
        env_config = await EnvironmentsService.get_request_config_services(
            query_db,
            EnvironmentsConfig(id=env_id)
        )

        # 创建执行器上下文
        api_executor_context = ExecutorContext(
            user_id=1,
            env_id=env_id,
            parameterization_id=param_item_data.get("parameterization_id"),
            parameterization=item_data,
            variables={},
            redis_obj=redis,
            mysql_obj=query_db,
            env_config=env_config,
            session=session
        )

        # 获取工作流
        workflow = await WorkflowService.get_workflow_nodetree_services(query_db, workflow_id)

        # 创建执行器
        executor = StreamingWorkflowExecutor()

        print(f"[进程 {process_id}][{group_name}] 开始执行工作流 ID: {workflow_id}")
        print("=" * 60)

        # 执行工作流
        async for event in executor.execute_workflow_stream(
                workflow=workflow,
                executor_context=api_executor_context
        ):
            timestamp = event.timestamp.strftime("%H:%M:%S")

            if event.node_id:
                print(
                    f"[进程{process_id}][{group_name}][{timestamp}] "
                    f"[{event.event_type.value.upper()}] [节点{event.node_id}] {event.message}"
                )
            else:
                print(
                    f"[进程{process_id}][{group_name}][{timestamp}] "
                    f"[{event.event_type.value.upper()}] {event.message}"
                )

            if event.progress is not None:
                print(f"[进程{process_id}][{group_name}]    >> 进度: {event.progress:.1f}%")

            if event.data and "task_result" in event.data:
                result = event.data["task_result"]
                print(f"[进程{process_id}][{group_name}]    >> 任务结果: {result}")

        print("=" * 60)
        print(f"[进程 {process_id}][{group_name}] 工作流执行完成")

        return {
            "success": True,
            "process_id": process_id,
            "group_name": group_name,
            "item": item_data
        }

    except Exception as e:
        print(f"[进程 {process_id}] 执行失败: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "process_id": process_id,
            "group_name": param_item_data.get("group_name", "Unknown"),
            "error": str(e)
        }
    finally:
        # 🔧 修复：按正确顺序关闭资源

        # 1. 关闭Redis (不依赖事件循环)
        if redis:
            try:
                await redis.close()
            except Exception as e:
                logger.debug(f"关闭Redis失败(忽略): {e}")

        # 2. 关闭HTTP session
        if session:
            try:
                await session.close()
                await asyncio.sleep(0.05)  # 给连接器时间完全关闭
            except Exception as e:
                logger.debug(f"关闭HTTP session失败(忽略): {e}")

        # 3. 关闭数据库generator (让它自动管理资源)
        if db_gen:
            try:
                await db_gen.aclose()
            except Exception as e:
                logger.debug(f"关闭数据库generator失败(忽略): {e}")

        # 4. 关闭HTTP generator
        if http_gen:
            try:
                await http_gen.aclose()
            except Exception as e:
                logger.debug(f"关闭HTTP generator失败(忽略): {e}")


async def execute_workflow_multiprocess(workflow_id: int, max_processes: int = 3):
    """
    使用多进程并发执行工作流

    优点：
    - 真正的并行执行（绕过 GIL）
    - 进程间完全隔离，互不影响
    - 适合 CPU 密集型任务
    - 某个进程崩溃不影响其他进程

    缺点：
    - 启动开销大
    - 内存占用高（每个进程独立内存）
    - 进程间通信复杂
    - 不能共享内存对象

    Args:
        workflow_id: 工作流ID
        max_processes: 最大进程数，建议 CPU 核心数
    """
    async for query_db in get_db():
        try:
            # 获取工作流基本信息
            workflow = await WorkflowService.get_workflow_nodetree_services(query_db, workflow_id)

            env_id = workflow.execution_config.env_id
            if not env_id:
                logger.error('环境为空，无法执行')
                return '环境为空，无法执行'

            # 获取所有参数化数据集
            api_param_item_page_query_result = await Api_param_itemDao.get_api_param_item_orm_list(
                query_db,
                Api_param_itemPageQueryModel(parameterization_id=6)
            )

            if not api_param_item_page_query_result:
                api_param_item_page_query_result = [Api_param_itemPageQueryModel(**dict())]

            # 将 Pydantic 模型转换为字典（进程间传递需要序列化）
            param_items_data = [
                {
                    "group_name": item.group_name,
                    "item": item.item,
                    "parameterization_id": item.parameterization_id
                }
                for item in api_param_item_page_query_result
            ]

            total_items = len(param_items_data)
            cpu_count = mp.cpu_count()

            logger.info("=" * 80)
            logger.info(f"多进程执行模式")
            logger.info(f"总数据集: {total_items}")
            logger.info(f"最大进程数: {max_processes}")
            logger.info(f"CPU 核心数: {cpu_count}")
            logger.info(f"推荐进程数: {min(max_processes, cpu_count)}")
            logger.info("=" * 80)

            start_time = datetime.now()

            # 使用进程池执行
            # 注意：必须在 if __name__ == '__main__' 保护下使用
            with mp.Pool(processes=max_processes) as pool:
                # 准备参数列表
                tasks = [
                    (workflow_id, param_data, env_id, idx)
                    for idx, param_data in enumerate(param_items_data)
                ]

                logger.info(f"启动 {max_processes} 个进程开始执行...")

                # 使用 starmap 并发执行（阻塞直到所有任务完成）
                results = pool.starmap(execute_param_item_in_process, tasks)

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            # 统计结果
            success_count = sum(1 for r in results if r.get("success"))
            failed_count = len(results) - success_count

            logger.info("=" * 80)
            logger.info(f"多进程执行完成！")
            logger.info(f"总执行时间: {execution_time:.2f}秒")
            logger.info(f"平均每个数据集: {execution_time / len(results):.2f}秒")
            logger.info(f"总数据集: {len(results)}")
            logger.info(f"成功: {success_count}")
            logger.info(f"失败: {failed_count}")
            logger.info("=" * 80)

            # 打印失败详情
            for result in results:
                if not result.get("success"):
                    logger.error(
                        f"失败数据集: {result.get('group_name')} "
                        f"(进程 {result.get('process_id')}) - "
                        f"错误: {result.get('error')}"
                    )

            return results

        except Exception as e:
            logger.error(f"多进程执行失败: {e}")
            traceback.print_exc()
            return None
        finally:
            await query_db.close()


async def execute_workflow_multiprocess_async(workflow_id: int, max_processes: int = 3):
    """
    使用多进程并发执行（异步非阻塞版本）

    使用 ProcessPoolExecutor + asyncio 实现异步多进程
    """
    from concurrent.futures import ProcessPoolExecutor

    async for query_db in get_db():
        try:
            workflow = await WorkflowService.get_workflow_nodetree_services(query_db, workflow_id)

            env_id = workflow.execution_config.env_id
            if not env_id:
                logger.error('环境为空，无法执行')
                return '环境为空，无法执行'

            api_param_item_page_query_result = await Api_param_itemDao.get_api_param_item_orm_list(
                query_db,
                Api_param_itemPageQueryModel(parameterization_id=6)
            )

            if not api_param_item_page_query_result:
                api_param_item_page_query_result = [Api_param_itemPageQueryModel(**dict())]

            param_items_data = [
                {
                    "group_name": item.group_name,
                    "item": item.item,
                    "parameterization_id": item.parameterization_id
                }
                for item in api_param_item_page_query_result
            ]

            logger.info("=" * 80)
            logger.info(f"异步多进程执行模式")
            logger.info(f"总数据集: {len(param_items_data)}")
            logger.info(f"最大进程数: {max_processes}")
            logger.info("=" * 80)

            start_time = datetime.now()

            # 使用 ProcessPoolExecutor 配合 asyncio
            loop = asyncio.get_event_loop()

            with ProcessPoolExecutor(max_workers=max_processes) as executor:
                # 创建任务列表
                tasks = [
                    loop.run_in_executor(
                        executor,
                        execute_param_item_in_process,
                        workflow_id,
                        param_data,
                        env_id,
                        idx
                    )
                    for idx, param_data in enumerate(param_items_data)
                ]

                logger.info(f"启动 {max_processes} 个进程（异步模式）...")

                # 异步等待所有任务完成
                results = await asyncio.gather(*tasks, return_exceptions=True)

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
            failed_count = len(results) - success_count

            logger.info("=" * 80)
            logger.info(f"异步多进程执行完成！")
            logger.info(f"总执行时间: {execution_time:.2f}秒")
            logger.info(f"平均每个数据集: {execution_time / len(results):.2f}秒")
            logger.info(f"总数据集: {len(results)}")
            logger.info(f"成功: {success_count}")
            logger.info(f"失败: {failed_count}")
            logger.info("=" * 80)

            for result in results:
                if isinstance(result, dict) and not result.get("success"):
                    logger.error(
                        f"失败数据集: {result.get('group_name')} - "
                        f"错误: {result.get('error')}"
                    )

            return results

        except Exception as e:
            logger.error(f"执行失败: {e}")
            traceback.print_exc()
            return None
        finally:
            await query_db.close()


async def demo(mode: str = "multiprocess", workflow_id: int = 1, max_workers: int = 3):
    """
    主函数

    Args:
        mode: 执行模式
            - "multiprocess": 多进程（阻塞版本）
            - "multiprocess_async": 异步多进程（非阻塞版本）
        workflow_id: 工作流ID
        max_workers: 最大进程数（建议不超过 CPU 核心数）
    """
    try:
        if mode == "multiprocess":
            logger.info("🔴 使用多进程执行模式（阻塞）")
            await execute_workflow_multiprocess(workflow_id, max_workers)

        elif mode == "multiprocess_async":
            logger.info("🟣 使用异步多进程执行模式（非阻塞）")
            await execute_workflow_multiprocess_async(workflow_id, max_workers)

        else:
            logger.error(f"不支持的模式: {mode}")

    except Exception as e:
        logger.error(f"执行出错: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    # ⚠️ 重要：多进程必须在 if __name__ == '__main__' 保护下运行

    # 获取 CPU 核心数
    cpu_cores = mp.cpu_count()
    print(f"当前系统 CPU 核心数: {cpu_cores}")

    # 方式1: 多进程（阻塞版本，推荐）
    asyncio.run(demo(mode="multiprocess", workflow_id=1, max_workers=8))

    # 方式2: 异步多进程（非阻塞版本）
    # asyncio.run(demo(mode="multiprocess_async", workflow_id=1, max_workers=3))
