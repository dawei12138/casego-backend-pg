FROM redis:7.2-alpine

# 设置时区
ENV TZ=Asia/Shanghai

# 复制配置文件（context 是项目根目录）
COPY ./CICD/docker/redis/redis.conf /usr/local/etc/redis/redis.conf

# 暴露端口
EXPOSE 6379

# 启动 Redis
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
