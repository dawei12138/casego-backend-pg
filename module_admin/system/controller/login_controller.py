import time

import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from config.enums import RedisInitKeyConfig, BusinessType
from config.env import AppConfig, JwtConfig
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from utils.ip_util import get_login_info
from module_admin.system.entity.vo.login_vo import UserLogin, UserRegister, Token
from module_admin.system.entity.vo.user_vo import CurrentUserModel, EditUserModel
from module_admin.system.service.login_service import CustomOAuth2PasswordRequestForm, LoginService, oauth2_scheme
from module_admin.system.service.user_service import UserService
from utils.log_util import logger
from utils.response_util import ResponseUtil


loginController = APIRouter()


@loginController.post('/login', response_model=Token)
@Log(title='用户登录', business_type=BusinessType.OTHER, log_type='login')
async def login(
    request: Request, form_data: CustomOAuth2PasswordRequestForm = Depends(), query_db: AsyncSession = Depends(get_db)
):
    t0 = time.time()

    # 0️⃣ 后端获取登录信息（IP、地区、浏览器、操作系统）
    login_info = get_login_info(request)

    # 1️⃣ 验证码启用状态检查
    t1 = time.time()
    captcha_enabled = (
        True
        if await request.app.state.redis.get(f'{RedisInitKeyConfig.SYS_CONFIG.key}:sys.account.captchaEnabled')
        == 'true'
        else False
    )
    t2 = time.time()
    logger.info(form_data)
    # 2️⃣ 用户认证
    user = UserLogin(
        userName=form_data.username,
        password=form_data.password,
        code=form_data.code,
        uuid=form_data.uuid,
        loginInfo=login_info,  # 使用后端获取的登录信息
        captchaEnabled=captcha_enabled,
    )
    result = await LoginService.authenticate_user(request, query_db, user)
    t3 = time.time()

    # 3️⃣ 生成 Token
    access_token_expires = timedelta(minutes=JwtConfig.jwt_expire_minutes)
    session_id = str(uuid.uuid4())
    access_token = await LoginService.create_access_token(
        data={
            'user_id': str(result[0].user_id),
            'user_name': result[0].user_name,
            'dept_name': result[1].dept_name if result[1] else None,
            'session_id': session_id,
            'login_info': user.login_info,
        },
        expires_delta=access_token_expires,
    )
    t4 = time.time()

    # 4️⃣ 写入 Redis
    if AppConfig.app_same_time_login:
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}',
            access_token,
            ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
        )
    else:
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{result[0].user_id}',
            access_token,
            ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
        )
    t5 = time.time()

    # 5️⃣ 更新用户信息
    await UserService.edit_user_services(
        query_db, EditUserModel(userId=result[0].user_id, loginDate=datetime.now(), type='status')
    )
    t6 = time.time()

    logger.info(
        f"[登录耗时统计] 总耗时: {(t6 - t0):.3f}s | 验证码检查: {(t2 - t1):.3f}s | 用户认证: {(t3 - t2):.3f}s | "
        f"生成Token: {(t4 - t3):.3f}s | 写入Redis: {(t5 - t4):.3f}s | 更新用户: {(t6 - t5):.3f}s"
    )

    logger.info('登录成功')

    # 6️⃣ 返回结果
    request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get('referer') else False
    request_from_redoc = request.headers.get('referer').endswith('redoc') if request.headers.get('referer') else False
    if request_from_swagger or request_from_redoc:
        return {'access_token': access_token, 'token_type': 'Bearer'}
    return ResponseUtil.success(msg='登录成功', dict_content={'token': access_token})


@loginController.get('/getInfo', response_model=CurrentUserModel)
async def get_login_user_info(
    request: Request, current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    logger.info('获取成功')

    return ResponseUtil.success(model_content=current_user)


@loginController.get('/getRouters')
async def get_login_user_routers(
    request: Request,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info('获取成功')
    user_routers = await LoginService.get_current_user_routers(current_user.user.user_id, query_db)

    return ResponseUtil.success(data=user_routers)


@loginController.post('/register', response_model=CrudResponseModel)
async def register_user(request: Request, user_register: UserRegister, query_db: AsyncSession = Depends(get_db)):
    user_register_result = await LoginService.register_user_services(request, query_db, user_register)
    logger.info(user_register_result.message)

    return ResponseUtil.success(data=user_register_result, msg=user_register_result.message)


# @loginController.post("/getSmsCode", response_model=SmsCode)
# async def get_sms_code(request: Request, user: ResetUserModel, query_db: AsyncSession = Depends(get_db)):
#     try:
#         sms_result = await LoginService.get_sms_code_services(request, query_db, user)
#         if sms_result.is_success:
#             logger.info('获取成功')
#             return ResponseUtil.success(data=sms_result)
#         else:
#             logger.warning(sms_result.message)
#             return ResponseUtil.failure(msg=sms_result.message)
#     except Exception as e:
#         logger.exception(e)
#         return ResponseUtil.error(msg=str(e))
#
#
# @loginController.post("/forgetPwd", response_model=CrudResponseModel)
# async def forget_user_pwd(request: Request, forget_user: ResetUserModel, query_db: AsyncSession = Depends(get_db)):
#     try:
#         forget_user_result = await LoginService.forget_user_services(request, query_db, forget_user)
#         if forget_user_result.is_success:
#             logger.info(forget_user_result.message)
#             return ResponseUtil.success(data=forget_user_result, msg=forget_user_result.message)
#         else:
#             logger.warning(forget_user_result.message)
#             return ResponseUtil.failure(msg=forget_user_result.message)
#     except Exception as e:
#         logger.exception(e)
#         return ResponseUtil.error(msg=str(e))


@loginController.post('/logout')
async def logout(request: Request, token: Optional[str] = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, JwtConfig.jwt_secret_key, algorithms=[JwtConfig.jwt_algorithm], options={'verify_exp': False}
        )
        if AppConfig.app_same_time_login:
            token_id: str = payload.get('session_id')
        else:
            token_id: str = payload.get('user_id')
        await LoginService.logout_services(request, token_id)
    except Exception as e:
        # token 无效时（过期、签名错误等），仍允许正常退出
        logger.warning(f'退出时token解析失败: {e}')

    logger.info('退出成功')
    return ResponseUtil.success(msg='退出成功')
