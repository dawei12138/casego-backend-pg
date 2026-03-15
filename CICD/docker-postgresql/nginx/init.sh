#!/bin/bash

# 初始化脚本：容器首次创建时初始化配置，后续使用宿主机映射配置（支持热更新）
# 此脚本放在 /docker-entrypoint.d/ 目录，nginx 镜像会在启动时自动执行

set -e

echo "========================================="
echo "开始初始化 Nginx 服务目录..."
echo "========================================="

# 1. 初始化配置目录（优先检查，确保 Nginx 能启动）
NGINX_CONF_DIR="/etc/nginx/conf.d"
DEFAULT_CONF="/tmp/nginx-default/nginx.conf"
TARGET_CONF="${NGINX_CONF_DIR}/default.conf"

echo "检查 Nginx 配置目录: ${NGINX_CONF_DIR}"

# 确保目录存在
mkdir -p ${NGINX_CONF_DIR}

# 检查是否存在任何 .conf 文件（目录可能有其他文件但没有配置）
CONF_COUNT=$(find ${NGINX_CONF_DIR} -maxdepth 1 -name "*.conf" 2>/dev/null | wc -l)

if [ "$CONF_COUNT" -eq 0 ]; then
    echo "检测到配置目录没有 .conf 文件（首次创建容器）"
    echo "正在复制默认配置文件到映射目录..."

    # 复制默认配置到映射目录，宿主机卷也会同步获得此文件
    if [ -f "${DEFAULT_CONF}" ]; then
        cp -f ${DEFAULT_CONF} ${TARGET_CONF}
        echo "✓ 配置文件已复制: ${TARGET_CONF}"
        echo "✓ 宿主机映射卷现在也有此配置文件"
    else
        echo "✗ 错误：未找到默认配置文件 ${DEFAULT_CONF}"
        exit 1
    fi
else
    echo "检测到配置目录已有 ${CONF_COUNT} 个 .conf 文件"
    echo "✓ 使用宿主机映射的配置（支持热更新: nginx -s reload）"
fi

echo "========================================="

# 2. 初始化前端文件目录
HTML_DIR="/data/html"
DEFAULT_HTML="/tmp/nginx-default"

echo "检查前端文件目录: ${HTML_DIR}"

# 确保目录存在
mkdir -p ${HTML_DIR}

# 检查映射目录是否为空
if [ -z "$(ls -A ${HTML_DIR} 2>/dev/null)" ]; then
    echo "检测到前端目录为空（首次创建容器）"
    echo "正在复制默认前端文件到映射目录..."

    # 只复制非配置文件（排除 nginx.conf）
    for item in ${DEFAULT_HTML}/*; do
        filename=$(basename "$item")
        if [ "$filename" != "nginx.conf" ]; then
            cp -r "$item" ${HTML_DIR}/
        fi
    done

    echo "✓ 前端文件已复制到映射目录"
    echo "✓ 宿主机映射卷现在也有这些文件"
else
    echo "检测到前端目录已有文件（宿主机已有前端）"
    echo "✓ 使用宿主机映射的前端文件（支持热更新）"
fi

echo "========================================="
echo "Nginx 初始化完成，准备启动服务..."
echo "=========================================
配置说明:
- 配置目录: ${NGINX_CONF_DIR} (修改后执行 nginx -s reload)
- 前端目录: ${HTML_DIR}
========================================="
