import inspect
import json
import os
import requests
import time
from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse, ORJSONResponse, UJSONResponse
from functools import lru_cache, wraps
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Callable, Literal, Optional
from user_agents import parse
from config.enums import BusinessType
from config.env import AppConfig
from exceptions.exception import LoginException, ServiceException, ServiceWarning
from module_admin.system.entity.vo.log_vo import LogininforModel, OperLogModel
from module_admin.system.service.log_service import LoginLogService, OperationLogService
from module_admin.system.service.login_service import LoginService
from utils.log_util import logger
from utils.response_util import ResponseUtil
from utils.ip_util import get_client_ip, get_ip_location as get_ip_location_util


class Log:
    """
    日志装饰器
    """

    def __init__(
        self,
        title: str,
        business_type: BusinessType,
        log_type: Optional[Literal['login', 'operation']] = 'operation',
    ):
        """
        日志装饰器

        :param title: 当前日志装饰器装饰的模块标题
        :param business_type: 业务类型（OTHER其它 INSERT新增 UPDATE修改 DELETE删除 GRANT授权 EXPORT导出 IMPORT导入 FORCE强退 GENCODE生成代码 CLEAN清空数据）
        :param log_type: 日志类型（login表示登录日志，operation表示为操作日志）
        :return:
        """
        self.title = title
        self.business_type = business_type.value
        self.log_type = log_type

    def __call__(self, func):
        # start_time_test = time.time()  # 时间测试
        @wraps(func)
        async def wrapper(*args, **kwargs):
            t0 = time.time()

            # 参数解析开始
            t_param_start = time.time()
            # ================= 参数解析区域 =================
            file_path = inspect.getfile(func)
            project_root = os.getcwd()
            relative_path = os.path.relpath(file_path, start=project_root)[0:-2].replace('\\', '.').replace('/', '.')
            func_path = f'{relative_path}{func.__name__}()'

            request_name_list = get_function_parameters_name_by_type(func, Request)
            request = get_function_parameters_value_by_name(func, request_name_list[0], *args, **kwargs)
            token = request.headers.get('Authorization')

            session_name_list = get_function_parameters_name_by_type(func, AsyncSession)
            query_db = get_function_parameters_value_by_name(func, session_name_list[0], *args, **kwargs)

            request_method = request.method
            # =============================================
            t_param_end = time.time()

            # 调用原始函数
            t_func_start = time.time()
            try:
                result = await func(*args, **kwargs)
            except (LoginException, ServiceWarning) as e:
                logger.warning(e.message)
                result = ResponseUtil.failure(data=e.data, msg=e.message)
            except ServiceException as e:
                logger.error(e.message)
                result = ResponseUtil.error(data=e.data, msg=e.message)
            except Exception as e:
                logger.exception(e)
                result = ResponseUtil.error(msg=str(e))
            t_func_end = time.time()

            # 响应结果处理
            t_resp_start = time.time()
            if isinstance(result, (JSONResponse, ORJSONResponse, UJSONResponse)):
                result_dict = json.loads(str(result.body, 'utf-8'))
            else:
                result_dict = {'code': getattr(result, "status_code", 500), 'message': '未知响应'}
            t_resp_end = time.time()

            # 日志写入
            t_log_start = time.time()
            try:
                if self.log_type == 'login':
                    # 登录日志记录
                    client_ip = get_client_ip(request)
                    login_location = get_ip_location_util(client_ip)
                    user_agent_str = request.headers.get('User-Agent', '')
                    user_agent = parse(user_agent_str)
                    browser = f'{user_agent.browser.family} {user_agent.browser.version_string}'
                    os_info = f'{user_agent.os.family} {user_agent.os.version_string}'

                    # 从请求体获取用户名
                    form_data_name_list = get_function_parameters_name_by_type(func, type(None))
                    user_name = ''
                    for name in kwargs:
                        param_value = kwargs.get(name)
                        if hasattr(param_value, 'username'):
                            user_name = param_value.username
                            break

                    # 判断登录状态
                    status = '0' if result_dict.get('code') == 200 else '1'
                    msg = result_dict.get('msg', '登录成功' if status == '0' else '登录失败')

                    login_log = LogininforModel(
                        userName=user_name,
                        ipaddr=client_ip,
                        loginLocation=login_location,
                        browser=browser,
                        os=os_info,
                        status=status,
                        msg=msg,
                        loginTime=datetime.now()
                    )
                    await LoginLogService.add_login_log_services(query_db, login_log)
                    logger.info(f'登录日志记录成功: {user_name} - {client_ip} - {login_location}')

                elif self.log_type == 'operation':
                    # 操作日志记录（如需要可在此添加）
                    pass
            except Exception as e:
                logger.warning(f'日志记录失败: {e}')
            t_log_end = time.time()

            # 总耗时
            t_end = time.time()

            logger.info(
                f"[日志装饰器耗时统计] 总耗时: {(t_end - t0):.3f}s | 参数解析: {(t_param_end - t_param_start):.3f}s | "
                f"函数执行: {(t_func_end - t_func_start):.3f}s | 响应处理: {(t_resp_end - t_resp_start):.3f}s | "
                f"日志写入: {(t_log_end - t_log_start):.3f}s"
            )

            return result

        # acquire_time = time.time() - start_time_test
        # logger.warning(f"日志记录器耗时: {acquire_time:.3f}s")
        return wrapper


@lru_cache()
def get_ip_location(oper_ip: str):
    """
    查询ip归属区域（使用VORE-API）

    :param oper_ip: 需要查询的ip
    :return: ip归属区域
    """
    # 直接调用ip_util中的函数，保持一致性
    return get_ip_location_util(oper_ip)


def get_function_parameters_name_by_type(func: Callable, param_type: Any):
    """
    获取函数指定类型的参数名称

    :param func: 函数
    :param arg_type: 参数类型
    :return: 函数指定类型的参数名称
    """
    # 获取函数的参数信息
    parameters = inspect.signature(func).parameters
    # 找到指定类型的参数名称
    parameters_name_list = []
    for name, param in parameters.items():
        if param.annotation == param_type:
            parameters_name_list.append(name)
    return parameters_name_list


def get_function_parameters_value_by_name(func: Callable, name: str, *args, **kwargs):
    """
    获取函数指定参数的值

    :param func: 函数
    :param name: 参数名
    :return: 参数值
    """
    # 获取参数值
    bound_parameters = inspect.signature(func).bind(*args, **kwargs)
    bound_parameters.apply_defaults()
    parameters_value = bound_parameters.arguments.get(name)

    return parameters_value
