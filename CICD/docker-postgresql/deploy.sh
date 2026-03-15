#!/bin/bash

# CaseGo 项目一键部署脚本 (PostgreSQL 独立版本)
# 使用方法: ./CICD/docker-postgresql/deploy.sh [build|start|stop|restart|logs|clean]
# 此脚本使用 CICD/docker-postgresql 目录下的独立配置，与 MySQL 版本完全隔离

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录，然后推导项目根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# docker-postgresql 目录在 CICD 下，所以项目根目录是往上两级
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "$PROJECT_ROOT"

COMPOSE_FILE="CICD/docker-postgresql/docker-compose.yml"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Docker 和 Docker Compose
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi

    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi

    log_info "Docker 和 Docker Compose 已就绪"
}

# 创建必要的目录
create_dirs() {
    log_info "创建必要的数据目录..."
    mkdir -p CICD/data-pg/postgresql
    mkdir -p CICD/data-pg/redis
    mkdir -p CICD/data-pg/backend
    mkdir -p CICD/data-pg/mcpserver
    mkdir -p CICD/data-pg/nginx/logs
    mkdir -p CICD/data-pg/nginx/html
    mkdir -p CICD/data-pg/nginx/conf.d
    log_info "目录创建完成"
}

# 构建镜像
build_images() {
    log_info "开始构建 Docker 镜像 (PostgreSQL 独立版本)..."

    log_info "构建 PostgreSQL 镜像..."
    docker compose -f ${COMPOSE_FILE} build postgres

    log_info "构建 Redis 镜像..."
    docker compose -f ${COMPOSE_FILE} build redis

    log_info "构建 Backend 镜像 (PostgreSQL)..."
    docker compose -f ${COMPOSE_FILE} build backend

    log_info "构建 MCP Server 镜像..."
    docker compose -f ${COMPOSE_FILE} build mcpserver

    log_info "构建 Nginx 镜像..."
    docker compose -f ${COMPOSE_FILE} build nginx

    log_info "所有镜像构建完成"
}

# 启动服务
start_services() {
    log_info "启动 CaseGo 服务 (PostgreSQL 独立版本)..."
    docker compose -f ${COMPOSE_FILE} up -d
    log_info "服务启动完成"

    log_info "等待服务就绪..."
    sleep 10

    log_info "服务状态:"
    docker compose -f ${COMPOSE_FILE} ps

    log_info ""
    log_info "========================================"
    log_info "CaseGo (PostgreSQL) 部署完成!"
    log_info "前端访问地址: http://localhost"
    log_info "后端 API 文档: http://localhost/docs"
    log_info "后端 Swagger: http://localhost/swagger-ui"
    log_info "数据库: PostgreSQL 15"
    log_info "网络: casego_pg_net (10.89.0.0/24)"
    log_info "数据目录: CICD/data-pg/"
    log_info "========================================"
}

# 停止服务
stop_services() {
    log_info "停止 CaseGo 服务 (PostgreSQL)..."
    docker compose -f ${COMPOSE_FILE} down
    log_info "服务已停止"
}

# 重启服务
restart_services() {
    log_info "重启 CaseGo 服务..."
    stop_services
    start_services
}

# 查看日志
view_logs() {
    log_info "查看服务日志 (Ctrl+C 退出)..."
    docker compose -f ${COMPOSE_FILE} logs -f
}

# 清理环境
clean_env() {
    log_warn "这将删除所有 PostgreSQL 版容器、镜像和数据，是否继续? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "清理环境..."
        docker compose -f ${COMPOSE_FILE} down -v --rmi all
        log_info "清理完成"
    else
        log_info "取消清理"
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
CaseGo 项目一键部署脚本 (PostgreSQL 独立版本)

使用方法:
  ./CICD/docker-postgresql/deploy.sh [命令]

命令:
  build      - 构建所有 Docker 镜像
  start      - 启动所有服务
  stop       - 停止所有服务
  restart    - 重启所有服务
  logs       - 查看服务日志
  clean      - 清理环境（删除容器、镜像、数据）
  help       - 显示帮助信息

数据库: PostgreSQL 15
网络: casego_pg_net (10.89.0.0/24)
数据目录: CICD/data-pg/
Compose 文件: ${COMPOSE_FILE}

与 MySQL 版本完全隔离:
  - 使用独立的 Docker 网络 (10.89.0.0/24 vs 10.88.0.0/24)
  - 使用独立的容器名称 (casego-pg-* vs casego-*)
  - 使用独立的数据目录 (CICD/data-pg/ vs CICD/data/)
  - 使用独立的镜像名称 (casego-pg-* vs casego-*)

示例:
  ./CICD/docker-postgresql/deploy.sh build     # 构建镜像
  ./CICD/docker-postgresql/deploy.sh start     # 启动服务
  ./CICD/docker-postgresql/deploy.sh logs      # 查看日志
EOF
}

# 主函数
main() {
    check_docker
    create_dirs

    case "${1:-}" in
        build)
            build_images
            ;;
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        logs)
            view_logs
            ;;
        clean)
            clean_env
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_info "执行完整部署流程 (PostgreSQL 独立版本)..."
            build_images
            start_services
            ;;
    esac
}

main "$@"
