FROM casego-backend:latest

ENV TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=prod

RUN apt-get update && apt-get install -y ca-certificates curl gnupg

# 导入 NodeSource GPG key（新版安全方式）
RUN mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
    | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# ⚠️ 这里改成 node_22.x
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" \
    > /etc/apt/sources.list.d/nodesource.list

# 安装 Node.js
RUN apt-get update && \
    apt-get install -y nodejs && \
    apt-get install -y --no-install-recommends rsync && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /tmp/app_src/requirements.txt
RUN pip install --no-cache-dir -r /tmp/app_src/requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/ \
    --extra-index-url https://pypi.org/simple \
    --trusted-host mirrors.aliyun.com \
    --timeout=120 \
    --retries=5

# 代码先放到 /tmp/app_src，不放 /app（防止被 volume 覆盖）
COPY ./ /tmp/app_src/

COPY ./CICD/docker-postgresql/backend/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 9099

CMD ["/start.sh"]