from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    """
    添加跨域中间件

    :param app: FastAPI对象
    :return:
    """
    # 前端页面url
    origins = [
        'http://localhost',
        'http://localhost:80',
        'http://127.0.0.1',
        'http://127.0.0.1:80',
        'http://localhost:8080',
        'http://127.0.0.1:8080',
        'http://localhost:9099',
        'http://127.0.0.1:9099',
    ]

    # 后台api允许跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # 开发环境允许所有来源
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
