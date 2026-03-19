FROM casego-backend:latest

# 设置环境变量
ENV TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=prod

# 设置工作目录
WORKDIR /app
# RUN npm install -g @playwright/cli@latest
# RUN npm install -g @playwright/mcp
# 先复制依赖文件，有变化才重新安装
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/ \
    --extra-index-url https://pypi.org/simple \
    --trusted-host mirrors.aliyun.com \
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
