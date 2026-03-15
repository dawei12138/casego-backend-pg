FROM postgres:16-alpine

# 设置时区
ENV TZ=Asia/Shanghai
ENV POSTGRES_DB=casego
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123456

# 设置语言环境
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# 复制初始化 SQL 脚本（context 是项目根目录）
# OPY ./CICD/docker-postgresql/postgresql/casego-pg.sql /docker-entrypoint-initdb.d/init.sql

# 暴露端口
EXPOSE 5432
