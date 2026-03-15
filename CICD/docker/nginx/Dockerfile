FROM nginx:1.25-alpine

# 设置时区
ENV TZ=Asia/Shanghai

# 安装必要工具
RUN apk add --no-cache bash

# 创建目录
# /data/html - 新的前端文件目录（保持为空，由 init.sh 初始化）
# /tmp/nginx-default - 存放默认前端文件和配置
RUN mkdir -p /data/html /etc/nginx/conf.d /tmp/nginx-default

# 复制前端 dist 文件到临时目录（作为默认文件备份）
# context 是项目根目录
COPY ./CICD/docker/nginx/dist/ /tmp/nginx-default/

# 复制 nginx 配置到临时目录（作为默认配置备份）
COPY ./CICD/docker/nginx/nginx.conf /tmp/nginx-default/nginx.conf

# 复制初始化脚本到 docker-entrypoint.d 目录（nginx 镜像会自动执行）
COPY ./CICD/docker/nginx/init.sh /docker-entrypoint.d/40-init-nginx-content.sh
RUN chmod +x /docker-entrypoint.d/40-init-nginx-content.sh

# 暴露端口
EXPOSE 80

# 启动 Nginx（使用默认 CMD）
CMD ["nginx", "-g", "daemon off;"]
