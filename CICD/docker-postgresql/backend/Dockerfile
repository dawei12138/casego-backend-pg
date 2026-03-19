FROM casego-backend:latest

ENV TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=prod

WORKDIR /app

COPY ./requirements.txt /tmp/app_src/requirements.txt
RUN pip install --no-cache-dir -r /tmp/app_src/requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/ \
    --extra-index-url https://pypi.org/simple \
    --trusted-host mirrors.aliyun.com \
    --timeout=120 \
    --retries=5 \

RUN apt install rsync

# 代码先放到 /tmp/app_src，不放 /app（防止被 volume 覆盖）
COPY ./ /tmp/app_src/

COPY ./CICD/docker-postgresql/backend/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 9099

CMD ["/start.sh"]