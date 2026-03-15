#!/bin/bash

set -e

echo "========================================="
echo "开始初始化后端应用目录..."
echo "========================================="

# 检查 /app 目录是否为空
APP_DIR="/app"
DEFAULT_CODE="/tmp/backend-default"

# 简单判断目录是否为空
if [ -z "$(ls -A ${APP_DIR} 2>/dev/null)" ]; then
    echo "检测到 ${APP_DIR} 目录为空"
    echo "正在从默认备份复制应用代码..."

    # 复制所有文件到 /app（包括隐藏文件如 .env.prod）
    # 使用 /. 语法确保复制所有文件，包括以点开头的隐藏文件
    cp -r ${DEFAULT_CODE}/. ${APP_DIR}/

    echo "✓ 默认应用代码复制完成"

    # 验证关键配置文件
    if [ -f "${APP_DIR}/.env.prod" ]; then
        echo "✓ .env.prod 配置文件已复制"
    else
        echo "⚠ 警告: .env.prod 配置文件未找到"
    fi
else
    echo "检测到 ${APP_DIR} 目录已有文件"
    echo "✓ 使用宿主机映射的代码"
fi

echo "========================================="
echo "应用目录初始化完成"
echo "========================================="

# ========================================
# 检测服务可用性的函数（使用 Python，最可靠）
# ========================================
check_port() {
    local host=$1
    local port=$2
    python3 -c "
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
try:
    result = sock.connect_ex(('$host', $port))
    sock.close()
    sys.exit(0 if result == 0 else 1)
except Exception as e:
    sys.exit(1)
"
}

# ========================================
# 等待 MySQL 就绪
# ========================================
echo "等待 MySQL 启动..."
MYSQL_HOST="${DB_HOST:-mysql}"
MYSQL_PORT="${DB_PORT:-3306}"

echo "目标地址: ${MYSQL_HOST}:${MYSQL_PORT}"

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if check_port "${MYSQL_HOST}" "${MYSQL_PORT}"; then
        echo "✓ MySQL 端口已就绪！"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "MySQL 未就绪 (尝试 ${RETRY_COUNT}/${MAX_RETRIES})，等待 3 秒..."
    sleep 3
done

if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "✗ MySQL 连接超时，但继续启动..."
else
    # 额外等待几秒，确保 MySQL 完全初始化
    echo "等待 MySQL 完全初始化..."
    sleep 5
    echo "✓ MySQL 连接成功！"
fi

# ========================================
# 等待 Redis 就绪
# ========================================
echo "等待 Redis 启动..."
REDIS_HOST="${REDIS_HOST:-redis}"
REDIS_PORT="${REDIS_PORT:-6379}"

echo "目标地址: ${REDIS_HOST}:${REDIS_PORT}"

RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if check_port "${REDIS_HOST}" "${REDIS_PORT}"; then
        echo "✓ Redis 端口已就绪！"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Redis 未就绪 (尝试 ${RETRY_COUNT}/${MAX_RETRIES})，等待 3 秒..."
    sleep 3
done

if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "✗ Redis 连接超时，但继续启动..."
else
    echo "✓ Redis 连接成功！"
fi

# 运行数据库迁移（如果需要）
# python -m alembic upgrade head

# 启动 FastAPI 应用
echo "========================================="
echo "启动 FastAPI 应用..."
echo "========================================="

# 从环境变量获取配置，设置默认值
APP_PORT="${APP_PORT:-9099}"
APP_WORKERS="${APP_WORKERS:-3}"

echo "端口: ${APP_PORT}, Workers: ${APP_WORKERS}"
exec uvicorn app:app --host 0.0.0.0 --port ${APP_PORT} --workers ${APP_WORKERS}
