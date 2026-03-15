# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based backend project (RuoYi-Vue3-FastAPI), an enterprise-grade application framework that includes API testing, workflow automation, user authentication, permission management, logging, and scheduled tasks.

## Development Commands

### Running the Application

```bash
# Install dependencies for MySQL
pip3 install -r requirements.txt

# Install dependencies for PostgreSQL
pip3 install -r requirements-pg.txt

# Run with specific environment (dev/prod)
python3 app.py --env=dev

# Using uvicorn directly (loads .env.dev by default)
uvicorn app:app --reload
```

The application runs on `http://localhost:9099` by default. API documentation is available at `http://localhost:9099/docs`.

### Database Setup

1. Create database `ruoyi-fastapi` (or your configured name)
2. Run the appropriate SQL script:
   - MySQL: `sql/ruoyi-fastapi.sql`
   - PostgreSQL: `sql/ruoyi-fastapi-pg.sql`
3. Configure connection in `.env.dev` or `.env.prod`

### Database Migrations (Alembic)

```bash
# Create a new manual migration
python -m alembic revision -m "description_of_changes"

# Apply all pending migrations
python -m alembic upgrade head

# Apply specific number of migrations
python -m alembic upgrade +1

# Downgrade to previous version
python -m alembic downgrade -1
```

**Important**: This project uses Alembic in manual mode due to AsyncSQL setup. Always write migrations manually rather than using auto-generation. Ensure database tables exist before applying migrations.

## Architecture

### Layered Architecture Pattern

The project follows a strict 4-layer MVC architecture:

1. **Controller** (`controller/`): Handles HTTP requests/responses, routing, and request validation
2. **Service** (`service/`): Implements business logic and orchestrates DAO calls
3. **DAO** (`dao/`): Data access layer, handles database operations using SQLAlchemy
4. **Entity** (`entity/`): Data models split into:
   - **DO** (Data Objects): SQLAlchemy ORM models mapped to database tables
   - **VO** (View Objects): Pydantic models for request/response validation

### Module Structure

```
module_admin/           # Main admin module
├── annotation/         # Decorators (logging, validation)
├── aspect/            # Cross-cutting concerns (auth, data scope)
├── system/            # System management (user, role, menu, dept, etc.)
├── api_project/       # API project management
├── api_project_submodules/  # Project submodules
├── api_testing/       # API testing framework
│   ├── api_test_cases/      # Test case management
│   ├── api_assertions/      # Assertion definitions
│   ├── api_environments/    # Environment configs
│   ├── api_databases/       # Database connections
│   ├── api_services/        # Service endpoints
│   ├── api_headers/         # Request headers
│   ├── api_params/          # Request params
│   ├── api_cookies/         # Cookie management
│   ├── api_formdata/        # Form data
│   ├── api_setup/           # Setup operations
│   ├── api_teardown/        # Teardown operations
│   ├── api_cache_data/      # Cache variables
│   └── api_test_execution_log/  # Execution logs
└── api_workflow/      # Workflow automation
    ├── workflow/            # Workflow definitions
    ├── api_worknodes/       # Workflow nodes
    ├── api_workflow_executions/     # Workflow execution logs
    ├── api_worknode_executions/     # Node execution logs
    ├── api_param_table/     # Parameter tables
    └── api_param_item/      # Parameter items

module_generator/      # Code generation module
module_task/          # Task scheduling module
module_fastmcp/       # MCP server integration (experimental)
```

### Key Components

**Configuration** (`config/`):
- `env.py`: Environment-based configuration using Pydantic settings, loads `.env.{env}` files
- `database.py`: Async SQLAlchemy engine and session factory
- `get_db.py`: Database session dependency injection
- `get_redis.py`: Redis connection pool management
- `get_scheduler.py`: APScheduler initialization for scheduled tasks
- `get_httpclient.py`: HTTP client configuration

**Middleware** (`middlewares/`):
- CORS middleware for cross-origin requests
- Gzip compression
- Trace middleware for request tracking
- Response time logging

**Exception Handling** (`exceptions/`):
- Custom exceptions: `AuthException`, `LoginException`, `PermissionException`, `ServiceException`, `ServiceWarning`
- Global exception handlers configured in `exceptions/handle.py`

**Decorators/Annotations** (`module_admin/annotation/`):
- `@Log(title, business_type)`: Automatic operation/login logging
- `@PydanticValidation`: Field validation decorator

**Aspects** (`module_admin/aspect/`):
- `CheckUserInterfaceAuth(perm)`: Permission-based access control
- `CheckRoleInterfaceAuth(role_key)`: Role-based access control
- `GetDataScope()`: Data scope filtering for multi-tenant scenarios

### API Testing & Workflow Features

This project includes a comprehensive API testing and workflow automation system:

**API Testing** (`utils/api_tools/executors/`):
- Execute API requests with full environment/variable support
- Database operations (MySQL queries)
- Python/JavaScript script execution
- Variable extraction from responses
- Assertion validation
- Setup/teardown operations

**Workflow System** (`utils/api_workflow_tools/`):
- Visual workflow designer support
- Node-based execution (API calls, DB operations, scripts)
- Parameter passing between nodes
- Workflow execution tracking and logging
- Parallel and sequential node execution

### Database Session Management

Use `Depends(get_db)` for database session injection:

```python
from config.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def some_endpoint(query_db: AsyncSession = Depends(get_db)):
    # Session automatically committed/rolled back
    pass
```

### Authentication Flow

1. User logs in via `/login` endpoint
2. JWT token generated and stored in Redis with TTL
3. Token passed in `Authorization` header for subsequent requests
4. `LoginService.get_current_user` dependency validates token and retrieves user
5. Permission decorators check user permissions/roles

### Application Startup Sequence

Defined in `server.py` lifespan:

1. Initialize database tables (`init_create_table`)
2. Create Redis connection pool
3. Load system dictionaries and configs into Redis
4. Initialize APScheduler for scheduled tasks
5. Run database connection tests

## Creating a New Module

Follow the layered architecture pattern (see `案例教程-创建自定义模块.md` for detailed example):

1. **Create DO** in `module_admin/{module}/entity/do/`: SQLAlchemy model
2. **Create VO** in `module_admin/{module}/entity/vo/`: Pydantic request/response models
3. **Create DAO** in `module_admin/{module}/dao/`: Database queries using AsyncSession
4. **Create Service** in `module_admin/{module}/service/`: Business logic layer
5. **Create Controller** in `module_admin/{module}/controller/`: FastAPI router with endpoints
6. **Register router** in `server.py`: Add to `controller_list`

### Module Naming Conventions

- Tables: `sys_*` prefix for system tables, `api_*` for API testing tables
- Classes: PascalCase (e.g., `SysUser`, `BookService`)
- Files: snake_case (e.g., `user_controller.py`, `book_service.py`)
- DO classes: Match table name in PascalCase (e.g., `SysUser` for `sys_user`)
- VO classes: Descriptive names with Model suffix (e.g., `UserQueryModel`, `BookDetailModel`)

## Environment Configuration

The project uses environment-specific `.env` files:
- `.env.dev`: Development environment
- `.env.prod`: Production environment

Configuration classes in `config/env.py`:
- `AppSettings`: Application settings (host, port, version, etc.)
- `JwtSettings`: JWT token configuration
- `DataBaseSettings`: Database connection (supports MySQL and PostgreSQL)
- `RedisSettings`: Redis connection
- `GenSettings`: Code generation settings
- `UploadSettings`: File upload configuration

## Logging

Use the centralized logger from `utils/log_util`:

```python
from utils.log_util import logger

logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.exception(exception)  # Logs exception with traceback
```

The `@Log` decorator automatically logs operations to the database.

## Response Format

All API responses use `ResponseUtil` from `utils/response_util`:

```python
from utils.response_util import ResponseUtil

# Success response
return ResponseUtil.success(data=result, msg="操作成功")

# Failure response
return ResponseUtil.failure(msg="操作失败")

# Error response
return ResponseUtil.error(msg="系统错误")

# Unauthorized
return ResponseUtil.unauthorized(msg="未授权")

# Forbidden
return ResponseUtil.forbidden(msg="无权限")
```

Standard response format:
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {...}
}
```

## Code Generation

Use the generator module to scaffold new modules:
- Access via `/system/gen` endpoints
- Configure in `config/env.py` `GenSettings`
- Generates DO, VO, DAO, Service, and Controller layers
- Output to `CaseGo/gen_path/`

## Testing Infrastructure

The project includes a sophisticated API testing system that supports:
- Multi-environment configuration
- Variable extraction and substitution using `${variable}` syntax
- Setup/teardown operations
- Database validations
- Python/JavaScript script execution
- Cookie and header management
- Response assertions

Test execution is tracked in `api_test_execution_log` with full request/response details.
