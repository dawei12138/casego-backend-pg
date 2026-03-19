#!/bin/bash

set -e

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
# 等待 PostgreSQL 就绪
# ========================================
echo "等待 PostgreSQL 启动..."
PG_HOST="${DB_HOST:-postgres}"
PG_PORT="${DB_PORT:-5432}"

echo "目标地址: ${PG_HOST}:${PG_PORT}"

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if check_port "${PG_HOST}" "${PG_PORT}"; then
        echo "PostgreSQL 端口已就绪！"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "PostgreSQL 未就绪 (尝试 ${RETRY_COUNT}/${MAX_RETRIES})，等待 3 秒..."
    sleep 3
done

if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "PostgreSQL 连接超时，但继续启动..."
else
    # 额外等待几秒，确保 PostgreSQL 完全初始化
    echo "等待 PostgreSQL 完全初始化..."
    sleep 5
    echo "PostgreSQL 连接成功！"
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
        echo "Redis 端口已就绪！"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Redis 未就绪 (尝试 ${RETRY_COUNT}/${MAX_RETRIES})，等待 3 秒..."
    sleep 3
done

if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "Redis 连接超时，但继续启动..."
else
    echo "Redis 连接成功！"
fi
# ========================================
# 同步代码到 /app（解决 volume 覆盖问题）
# ========================================
echo "同步代码文件..."

# 确保 /app 目录存在
mkdir -p /app

# --update: 源文件比目标文件新才覆盖，用户数据文件不受影响
# --checksum: 按内容比较而不是时间戳（更可靠）
rsync -av --update --checksum /tmp/app_src/ /app/

echo "代码同步完成！"

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
