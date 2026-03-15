import requests
from fastapi import Request
from functools import lru_cache
from utils.log_util import logger


def get_client_ip(request: Request) -> str:
    """
    获取客户端真实IP地址

    优先级: X-Real-IP > X-Forwarded-For > client.host

    :param request: FastAPI Request对象
    :return: 客户端IP地址
    """
    # 1. Nginx配置的真实IP头 (推荐)
    x_real_ip = request.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip.strip()

    # 2. 代理转发的IP链（取第一个，即原始客户端IP）
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # X-Forwarded-For格式: client, proxy1, proxy2
        return x_forwarded_for.split(',')[0].strip()

    # 3. 直接连接的客户端IP
    if request.client:
        return request.client.host

    return '127.0.0.1'


def is_internal_ip(ip: str) -> bool:
    """
    判断是否为内网IP

    :param ip: IP地址
    :return: 是否为内网IP
    """
    if not ip or ip in ('127.0.0.1', 'localhost', '::1'):
        return True

    # 检查是否为内网IP段
    if ip.startswith(('10.', '192.168.')):
        return True

    # 172.16.0.0 - 172.31.255.255
    if ip.startswith('172.'):
        parts = ip.split('.')
        if len(parts) >= 2:
            try:
                second_octet = int(parts[1])
                if 16 <= second_octet <= 31:
                    return True
            except ValueError:
                pass

    return False


@lru_cache(maxsize=1024)
def get_ip_location(ip: str) -> str:
    """
    查询IP归属地区（使用VORE-API）

    API文档: https://api.vore.top/api/IPdata?ip=xxx
    返回格式如: "中国-广东省-深圳市" 或 "美国-弗吉尼亚州"

    :param ip: IP地址
    :return: 归属地区
    """
    if is_internal_ip(ip):
        return '内网IP'

    try:
        response = requests.get(
            f'https://api.vore.top/api/IPdata?ip={ip}',
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                ipdata = result.get('ipdata', {})
                info1 = ipdata.get('info1', '')  # 国家
                info2 = ipdata.get('info2', '')  # 省/州
                info3 = ipdata.get('info3', '')  # 城市

                # 组装地区信息
                parts = [p for p in [info1, info2, info3] if p]
                if parts:
                    return '-'.join(parts)

                # 备用：使用adcode.n字段
                adcode = result.get('adcode', {})
                if adcode.get('n'):
                    return adcode.get('n')

    except Exception as e:
        logger.warning(f'查询IP地区失败: {ip}, 错误: {e}')

    return '未知'


@lru_cache(maxsize=1024)
def get_ip_detail(ip: str) -> dict:
    """
    获取IP详细信息（使用VORE-API）

    :param ip: IP地址
    :return: IP详细信息字典
    """
    default_result = {
        'ip': ip,
        'country': '',
        'province': '',
        'city': '',
        'isp': '',
        'location': '未知'
    }

    if is_internal_ip(ip):
        default_result['location'] = '内网IP'
        return default_result

    try:
        response = requests.get(
            f'https://api.vore.top/api/IPdata?ip={ip}',
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                ipdata = result.get('ipdata', {})
                info1 = ipdata.get('info1', '')  # 国家
                info2 = ipdata.get('info2', '')  # 省/州
                info3 = ipdata.get('info3', '')  # 城市
                isp = ipdata.get('isp', '')      # 运营商

                parts = [p for p in [info1, info2, info3] if p]
                location = '-'.join(parts) if parts else '未知'

                return {
                    'ip': ip,
                    'country': info1,
                    'province': info2,
                    'city': info3,
                    'isp': isp,
                    'location': location
                }

    except Exception as e:
        logger.warning(f'查询IP详情失败: {ip}, 错误: {e}')

    return default_result


def get_login_info(request: Request) -> dict:
    """
    获取登录信息（IP、地区、浏览器、操作系统等）

    :param request: FastAPI Request对象
    :return: 登录信息字典
    """
    from datetime import datetime
    from user_agents import parse

    # 获取真实IP
    client_ip = get_client_ip(request)

    # 获取IP归属地
    login_location = get_ip_location(client_ip)

    # 解析User-Agent
    user_agent_str = request.headers.get('User-Agent', '')
    user_agent = parse(user_agent_str)

    # 获取浏览器信息
    browser = f'{user_agent.browser.family} {user_agent.browser.version_string}'

    # 获取操作系统信息
    os = f'{user_agent.os.family} {user_agent.os.version_string}'

    return {
        'ipaddr': client_ip,
        'loginLocation': login_location,
        'browser': browser,
        'os': os,
        'loginTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
