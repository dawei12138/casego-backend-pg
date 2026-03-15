
<div align="center">

基于 FastAPI 的企业级 API 自动化测试平台

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 项目简介

CaseGo 是一个现代化的企业级 API 自动化测试平台，提供完整的测试管理、执行和报告功能。
### 演示地址
https://demo.1592653.xyz/

### 前端地址
https://gitee.com/dewei_wei/fast_api_admin_frontend
## 在线文档
[在线文档](http://8.130.23.175:88/)
### 系统图示

#### 用例管理
![用例管理](./CaseGo/download_path/用例管理.png)
#### 用例执行
![用例执行](./CaseGo/download_path/用例执行.png)
#### 自动化测试
![自动化测试](./CaseGo/download_path/自动化测试.png)
#### 定时任务
![定时任务](./CaseGo/download_path/定时任务.png)
### mcp服务
![mcp服务](./CaseGo/download_path/mcp服务.png)
### 自定义函数
![自定义函数](./CaseGo/download_path/自定义函数.png)
### 项目接口文档
![项目接口文档](./CaseGo/download_path/接口文档.png)
### 代码生成器
![代码生成器](./CaseGo/download_path/代码生成器.png)



### 核心功能

- 🚀 **API 自动化测试** - 支持 HTTP/HTTPS 接口测试，完整的断言和验证机制
- 🔄 **mcp支持** - 支持调用mcp服务自动生成参数化接口用例
- 🌍 **多环境管理** - 灵活的环境配置，支持开发/测试/生产环境切换
- 📊 **测试报告** - 详细的执行日志和可视化测试报告
- 🔐 **权限管理** - 基于 RBAC 的细粒度权限控制
- 💾 **数据库操作** - 支持测试前后的数据库操作（MySQL）
- 📝 **脚本扩展** - 支持 Python/JavaScript 自定义脚本执行
- 🎯 **参数化测试** - 变量提取、缓存和参数化支持

## 技术栈

- **后端框架**: FastAPI 0.115+
- **数据库**: MySQL 8.0+ 
- **缓存**: Redis 6.0+
- **ORM**: SQLAlchemy 2.0 (异步)
- **任务调度**: APScheduler
- **API 文档**: Swagger/OpenAPI

## 快速开始
### Docker 部署

```bash
# 使用 docker-compose
docker-compose up -d
```

### 环境要求

- Python 3.10+
- MySQL 8.0+ 
- Redis 6.0+

### 安装步骤

1. **克隆项目**

```bash
git clone https://gitee.com/dewei_wei/casego.git
cd casego
```

2. **安装依赖**

```bash
# 创建虚拟环境并安装依赖
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host pypi.mirrors.ustc.edu.cn --no-cache-dir
```

3. **配置数据库**

创建数据库并导入初始数据：

```sql
-- MySQL
CREATE DATABASE `casego` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 导入 SQL 脚本

```

4. **配置环境变量**

编辑 `.env.dev` 文件，配置数据库和 Redis 连接：

```env
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_DB=casego

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

5. **启动服务**

```bash
# 开发环境启动
python app.py --env=dev

# 或使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port ${APP_PORT} --workers ${APP_WORKERS}
```
>mcp服务启动
~~~
python -m module_fastmcp.mcp_server
~~~
6. **访问应用**

- 应用地址: http://localhost:9099
- mcp服务地址: http://localhost:8001/v1/mcp
- API 文档: http://localhost:9099/docs
- 默认账号: `admin` / `admin123`

## 项目结构

```
casego/
├── module_admin/              # 主业务模块
│   ├── system/               # 系统管理（用户、角色、菜单等）
│   ├── api_testing/          # API 测试模块
│   │   ├── api_test_cases/  # 测试用例
│   │   ├── api_environments/ # 环境配置
│   │   ├── api_assertions/  # 断言管理
│   │   └── ...
│   └── api_workflow/         # 工作流模块
├── config/                   # 配置文件
├── utils/                    # 工具类
├── middlewares/              # 中间件
├── exceptions/               # 异常处理
├── sql/                      # 数据库脚本
└── app.py                    # 应用入口
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT License](LICENSE)

---

如有问题，请查看 [详细文档](CLAUDE.md) 或提交 Issue。
