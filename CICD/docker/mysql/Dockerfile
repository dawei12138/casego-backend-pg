FROM mysql:8.0

# 设置时区
ENV TZ=Asia/Shanghai
ENV MYSQL_DATABASE=casego

# 复制初始化 SQL 脚本（context 是项目根目录）
COPY ./CICD/docker/mysql/casego.sql /docker-entrypoint-initdb.d/init.sql

# 设置字符集
RUN echo '[mysqld]' > /etc/mysql/conf.d/charset.cnf && \
    echo 'character-set-server=utf8mb4' >> /etc/mysql/conf.d/charset.cnf && \
    echo 'collation-server=utf8mb4_unicode_ci' >> /etc/mysql/conf.d/charset.cnf && \
    echo '[client]' >> /etc/mysql/conf.d/charset.cnf && \
    echo 'default-character-set=utf8mb4' >> /etc/mysql/conf.d/charset.cnf

# 暴露端口
EXPOSE 3306
