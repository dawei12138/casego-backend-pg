from datetime import datetime
from typing import Optional

from utils.log_util import logger


def job(*args, **kwargs):
    """
    定时任务执行同步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}同步函数执行了')


async def async_job(*args, **kwargs):
    """
    定时任务执行异步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}异步函数执行了')


async def run_workflow_task(
    workflow_id: int,
    user_id: int = 1,
    env_id: Optional[int] = None,
    parameterization_id: Optional[int] = None,
    loop_count: int = 1,
    lock_timeout: int = 300
):
    """
    定时任务：执行工作流（多 worker 模式下只执行一次）

    参数:
        workflow_id: 工作流ID（必填）
        user_id: 用户ID（默认1，用于接收通知）
        env_id: 环境ID（可选，从工作流配置获取）
        parameterization_id: 参数化ID（可选）
        loop_count: 循环次数（默认1）
        lock_timeout: 分布式锁超时时间（秒），默认5分钟

    使用示例:
        在定时任务配置中设置:
        - 调用目标: module_task.scheduler_test:run_workflow_task
        - 参数: {"workflow_id": 1, "user_id": 1}
    """
    import uuid
    from config.get_redis import RedisUtil
    from utils.api_workflow_tools.workflow_visual_executor import execute_workflow_sync

    # 生成唯一锁 key 和锁值（用于安全释放）
    # lock_key = f"workflow_task_lock:{workflow_id}"
    # lock_value = f"{uuid.uuid4()}:{datetime.now().isoformat()}"



    try:
        result = await execute_workflow_sync(
            workflow_id=workflow_id,
            user_id=user_id,
            env_id=env_id,
            parameterization_id=parameterization_id,
            loop_count=loop_count,
            trigger_type="cron"
        )

        if result:
            if result.get("isSuccess"):
                logger.info(
                    f"[定时任务] 工作流 {result.get('workflowName', workflow_id)} 执行成功: "
                    f"共{result['totalCases']}条, 成功{result['successCases']}条, "
                    f"耗时{result['duration']:.2f}秒"
                )
            else:
                logger.warning(
                    f"[定时任务] 工作流 {result.get('workflowName', workflow_id)} 执行完成但有失败: "
                    f"共{result['totalCases']}条, 失败{result['failedCases']}条"
                )
        return result

    except Exception as e:
        logger.error(f"[定时任务] 工作流 {workflow_id} 执行异常: {e}")
        raise

    finally:
        pass
