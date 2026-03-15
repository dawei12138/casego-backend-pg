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

# 设置工作目录
WORKDIR /app

# 先复制依赖文件并安装（利用 Docker 缓存）
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    -i https://pypi.mirrors.ustc.edu.cn/simple \
    --trusted-host pypi.mirrors.ustc.edu.cn \
    --timeout=120 \
    --retries=5

# 复制应用代码
COPY ./ /app/

# 复制启动脚本
COPY ./CICD/docker-postgresql/backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 暴露端口
EXPOSE 9099

# 启动应用
CMD ["/app/start.sh"]
