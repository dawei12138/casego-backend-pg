import uvicorn
from server import app, AppConfig  # noqa: F401

if __name__ == '__main__':
    print("启动服务...")

    uvicorn.run(
        app='app:app',
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        root_path=AppConfig.app_root_path,
        reload=AppConfig.app_reload,
        workers=AppConfig.app_workers
    )
