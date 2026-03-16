from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from config.database_ping import DatabaseTestUtil
from config.env import AppConfig
from config.get_db import init_create_table
from config.get_redis import RedisUtil, RedisProxy
from config.get_scheduler import SchedulerUtil
from config.get_websocket import websocket_manager
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware
from module_admin.api_testing.api_assertions.controller.assertions_controller import assertionsController
from module_admin.api_testing.api_cache_data.controller.cache_data_controller import cache_dataController
from module_admin.api_testing.api_cookies.controller.cookies_controller import cookiesController
from module_admin.api_testing.api_databases.controller.api_databases_controller import api_databasesController
from module_admin.api_testing.api_environments.controller.environments_controller import environmentsController
from module_admin.api_testing.api_formdata.controller.formdata_controller import formdataController
from module_admin.api_testing.api_headers.controller.headers_controller import headersController
from module_admin.api_testing.api_params.controller.params_controller import paramsController

from module_admin.api_project.controller.project_controller import projectController

from module_admin.api_project_submodules.controller.project_submodules_controller import project_submodulesController
from module_admin.api_testing.api_script_library.controller.script_library_controller import script_libraryController
from module_admin.api_testing.api_faker_func.faker_config_controller import fakerConfigController
from module_admin.api_testing.api_services.controller.services_controller import servicesController
from module_admin.api_testing.api_setup.controller.setup_controller import setupController
from module_admin.api_testing.api_teardown.controller.teardown_controller import teardownController
from module_admin.api_testing.api_test_cases.controller.test_cases_controller import test_casesController
from module_admin.api_testing.api_test_execution_log.controller.execution_log_controller import execution_logController
from module_admin.api_workflow.api_param_item.controller.api_param_item_controller import api_param_itemController
from module_admin.api_workflow.api_param_table.controller.api_param_table_controller import api_param_tableController
from module_admin.api_workflow.api_workflow_executions.controller.workflow_executions_controller import \
    workflow_executionsController
from module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller import \
    api_workflow_reportController
from module_admin.api_workflow.api_worknode_executions.controller.worknode_executions_controller import \
    worknode_executionsController
from module_admin.api_workflow.api_worknodes.controller.worknodes_controller import worknodesController
from module_admin.api_workflow.workflow.controller.workflow_controller import workflowController
from module_admin.system.notification.controller.notification_controller import notificationController
from module_admin.websocket.controller.websocket_controller import websocketController

from module_admin.system.controller.cache_controller import cacheController
from module_admin.system.controller.captcha_controller import captchaController
from module_admin.system.controller.common_controller import commonController
from module_admin.system.controller.config_controller import configController
from module_admin.system.controller.dept_controller import deptController
from module_admin.system.controller.dict_controller import dictController
from module_admin.system.controller.file_controller import fileController
from module_admin.system.controller.log_controller import logController
from module_admin.system.controller.login_controller import loginController
from module_admin.system.controller.job_controller import jobController
from module_admin.system.controller.menu_controller import menuController
from module_admin.system.controller.notice_controller import noticeController
from module_admin.system.controller.online_controller import onlineController
from module_admin.system.controller.post_controler import postController
from module_admin.system.controller.role_controller import roleController
from module_admin.system.controller.server_controller import serverController
from module_admin.system.controller.user_controller import userController
from module_app.agents.controller.agents_controller import agentsController
from module_app.cases.controller.cases_controller import casesController
from module_app.devices.controller.devices_controller import devicesController
from module_app.elements.controller.elements_controller import elementsController
from module_app.globalparams.controller.globalparams_controller import globalparamsController
from module_app.public_steps.controller.publicsteps_controller import publicstepsController
from module_app.steps.controller.steps_controller import stepsController
from module_app.steps_elements.controller.steps_elements_controller import steps_elementsController
from module_app.websocket import agentTransportController

from module_generator.controller.gen_controller import genController
from module_llm.chat_mcp_config.controller.mcpconfig_controller import mcpconfigController
from module_llm.chat_thread.controller.thread_controller import threadController

from module_llm.llm_provider.controller.provider_config_controller import provider_configController
from module_llm.chat_agent.controller.chat_controller import chatController
from module_llm.workspace.controller.workspace_controller import workspaceController
# from module_llm.chat_agent.graph import close_checkpointer

from sub_applications.handle import handle_sub_applications
from utils.common_util import worship
from utils.log_util import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动逻辑
    logger.info(f'{AppConfig.app_name}开始启动')
    worship()
    await init_create_table()

    # 创建 Redis 连接并使用 RedisProxy 包装，实现自动重连
    redis_instance = await RedisUtil.create_redis_pool()
    app.state.redis = RedisProxy(redis_instance)

    # 清理残留的调度器锁（防止异常退出导致锁未释放）
    await RedisUtil.clear_scheduler_locks(app.state.redis)

    # 初始化 WebSocket 管理器的 Redis Pub/Sub（支持多 Worker 跨进程通信）
    await websocket_manager.init_redis(redis_instance)

    await RedisUtil.init_sys_dict(app.state.redis)
    await RedisUtil.init_sys_config(app.state.redis)
    await SchedulerUtil.init_system_scheduler()
    await DatabaseTestUtil.run_full_connection_test(app)

    logger.info(f'{AppConfig.app_name}启动成功')
    yield

    # 清理逻辑
    # await close_checkpointer()
    await websocket_manager.close()
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()


# 初始化FastAPI对象
app = FastAPI(
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    lifespan=lifespan,
    docs_url=None,  # 禁用默认的 Swagger UI
    redoc_url=None,  # 禁用默认的 Redoc
)


# 自定义 OpenAPI schema，强制使用 3.0.3 版本以兼容旧版 Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # 将 OpenAPI 版本从 3.1.0 改为 3.0.3 以兼容旧版 Swagger UI
    openapi_schema["openapi"] = "3.0.3"
    # 添加 servers 配置，让 Swagger UI 请求带上 /dev-api 前缀
    openapi_schema["servers"] = [
        {"url": "/", "description": "本地环境"},
        {"url": "/dev-api", "description": "测试环境"},

    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# 挂载子应用
handle_sub_applications(app)
# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)

# 加载路由列表
controller_list = [
    {'router': loginController, 'tags': ['登录模块']},
    {'router': captchaController, 'tags': ['验证码模块']},
    {'router': userController, 'tags': ['系统管理-用户管理']},
    {'router': roleController, 'tags': ['系统管理-角色管理']},
    {'router': menuController, 'tags': ['系统管理-菜单管理']},
    {'router': deptController, 'tags': ['系统管理-部门管理']},
    {'router': postController, 'tags': ['系统管理-岗位管理']},
    {'router': dictController, 'tags': ['系统管理-字典管理']},
    {'router': configController, 'tags': ['系统管理-参数管理']},
    {'router': noticeController, 'tags': ['系统管理-通知公告管理']},
    {'router': logController, 'tags': ['系统管理-日志管理']},
    {'router': fileController, 'tags': ['系统管理-附件管理']},
    {'router': onlineController, 'tags': ['系统监控-在线用户']},
    {'router': jobController, 'tags': ['系统监控-定时任务']},
    {'router': serverController, 'tags': ['系统监控-菜单管理']},
    {'router': cacheController, 'tags': ['系统监控-缓存监控']},
    {'router': commonController, 'tags': ['通用模块']},
    {'router': genController, 'tags': ['代码生成']},
    {'router': projectController, 'tags': ['项目模块']},
    {'router': api_databasesController, 'tags': ['数据库模块']},
    {'router': environmentsController, 'tags': ['环境模块']},
    {'router': project_submodulesController, 'tags': ['项目子模块']},
    {'router': servicesController, 'tags': ['环境服务表']},
    {'router': cache_dataController, 'tags': ['环境緩存變量表']},
    {'router': test_casesController, 'tags': ['测试接口']},
    {'router': assertionsController, 'tags': ['接口断言']},
    {'router': cookiesController, 'tags': ['接口请求Cookie']},
    {'router': headersController, 'tags': ['接口请求头']},
    {'router': paramsController, 'tags': ['接口请求参数']},
    {'router': setupController, 'tags': ['接口前置操作']},
    {'router': teardownController, 'tags': ['接口后置操作']},
    {'router': formdataController, 'tags': ['接口的bodyfrom表单']},
    {'router': workflowController, 'tags': ['工作流基础信息']},
    {'router': workflow_executionsController, 'tags': ['工作流执行日志']},
    {'router': worknode_executionsController, 'tags': ['工作节点执行日志']},
    {'router': worknodesController, 'tags': ['工作流节点']},
    {'router': execution_logController, 'tags': ['接口执行日志']},
    {'router': api_param_tableController, 'tags': ['工作流参数表']},
    {'router': api_param_itemController, 'tags': ['工作流参数表横向']},
    {'router': api_workflow_reportController, 'tags': ['工作流报告']},
    {'router': websocketController, 'tags': ['WebSocket 路由']},
    {'router': notificationController, 'tags': ['通知消息']},
    {'router': script_libraryController, 'tags': ['公共脚本']},
    {'router': fakerConfigController, 'tags': ['Faker配置']},
    # {'router': casesController, 'tags': ['app测试用例']},
    # {'router': steps_elementsController, 'tags': ['app步骤-元素关联']},
    # {'router': elementsController, 'tags': ['app元素']},
    # {'router': stepsController, 'tags': ['app步骤']},
    # {'router': publicstepsController, 'tags': ['app公共步骤']},
    # {'router': globalparamsController, 'tags': ['app全局参数']},
    # {'router': agentsController, 'tags': ['app代理']},
    # {'router': agentTransportController, 'tags': ['app代理控制器']},
    # {'router': devicesController, 'tags': ['app设备驱动']},
    # {'router': llmRouter, 'tags': ['AI大模型']},
    {'router': threadController, 'tags': ['大模型对话线程']},
    {'router': provider_configController, 'tags': ['大模型配置']},
    {'router': chatController, 'tags': ['大模型对话']},
    {'router': workspaceController, 'tags': ['AI工作区文件管理']},
    {'router': mcpconfigController, 'tags': ['AImcp服务配置']},
    # {'router': testController, 'tags': ['测试的']},
]

for controller in controller_list:
    app.include_router(router=controller.get('router'), tags=controller.get('tags'))


# 挂载静态文件目录用于离线文档资源
app.mount("/static/swagger-ui", StaticFiles(directory="CaseGo/download_path/swagger-ui"), name="swagger-ui-static")
app.mount("/static/redoc", StaticFiles(directory="CaseGo/download_path/redoc"), name="redoc-static")


# 自定义 Swagger UI 文档端点（使用离线资源）
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon-32x32.png",
    )


# 自定义 Redoc 文档端点（使用离线资源）
@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
        redoc_favicon_url="/static/swagger-ui/favicon-32x32.png",
    )

