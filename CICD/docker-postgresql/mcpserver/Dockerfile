FROM my-fastapi-base:latest

# 设置环境变量
ENV TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=prod

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    curl \
    bash \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 创建临时目录用于存放默认代码
RUN mkdir -p /tmp/mcpserver-default

# 复制 requirements-pg.txt 到临时目录（使用 PostgreSQL 依赖）
COPY ./requirements-pg.txt /tmp/mcpserver-default/requirements-pg.txt

# 安装 Python 依赖（PostgreSQL 版本）
RUN pip install --no-cache-dir -r /tmp/mcpserver-default/requirements-pg.txt \
    -i https://pypi.mirrors.ustc.edu.cn/simple \
    --trusted-host pypi.mirrors.ustc.edu.cn \
    --timeout=120 \
    --retries=5

# 复制应用代码到临时目录（作为默认代码备份）
# context 是项目根目录，整个根目录就是后端代码
COPY ./ /tmp/mcpserver-default/

# 复制启动脚本到 /tmp/（不放在 /app 中）
COPY ./CICD/docker-postgresql/mcpserver/start.sh /tmp/start.sh
RUN chmod +x /tmp/start.sh

# 创建空的 /app 目录（保持为空，由启动脚本初始化）
RUN mkdir -p /app

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 8001

# 启动应用（使用 /tmp/ 下的启动脚本）
CMD ["/tmp/start.sh"]
