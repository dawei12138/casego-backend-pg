# -*- coding: utf-8 -*-
"""
Agent 消息处理器

负责处理来自 Sonic Agent 的各类 WebSocket 消息
对应 Java: TransportServerController 的消息处理逻辑
"""
from sqlalchemy.ext.asyncio import AsyncSession
from module_app.websocket.agent_manager import agent_manager
from module_app.enums import AgentStatusEnum, DeviceStatusEnum
from utils.log_util import logger


class AgentMessageHandler:
    """
    Agent 消息处理器

    处理来自 Agent 的各类消息，包括：
    - 心跳和状态管理
    - 设备信息上报
    - 用例步骤查询
    - 执行结果回调
    """

    def __init__(self, agent_id: int, db: AsyncSession):
        """
        初始化消息处理器

        :param agent_id: Agent ID
        :param db: 数据库会话
        """
        self.agent_id = agent_id
        self.db = db

    async def handle_message(self, msg: dict) -> None:
        """
        处理 Agent 消息的主入口

        根据消息类型路由到对应的处理方法

        :param msg: 消息内容
        """
        msg_type = msg.get('msg')

        if not msg_type:
            logger.warning(f'Agent {self.agent_id} 发送了无效消息: {msg}')
            return

        # 消息路由映射
        handler_map = {
            # P0 优先级 - 核心消息
            'ping': self._handle_ping,
            'heartBeat': self._handle_heartbeat,
            'agentInfo': self._handle_agent_info,
            'deviceDetail': self._handle_device_detail,
            'findSteps': self._handle_find_steps,

            # P1 优先级 - 重要消息
            'debugUser': self._handle_debug_user,
            'battery': self._handle_battery,
            'generateStep': self._handle_generate_step,
            'errCall': self._handle_error_callback,

            # P2 优先级 - 可选消息
            'subResultCount': self._handle_sub_result_count,
            'step': self._handle_step_result,
            'perform': self._handle_perform_result,
            'record': self._handle_record,
            'status': self._handle_status,
        }

        handler = handler_map.get(msg_type)
        if handler:
            try:
                await handler(msg)
            except Exception as e:
                logger.error(f'Agent {self.agent_id} 处理消息 {msg_type} 失败: {e}')
        else:
            logger.debug(f'Agent {self.agent_id} 未知消息类型: {msg_type}')

    # ==================== P0 核心消息处理 ====================

    async def _handle_ping(self, msg: dict) -> None:
        """
        处理 ping 消息（心跳）

        原始Sonic设计：
        - 客户端每10秒主动发送 {"msg":"ping"}
        - 服务端接收后立即回复 {"msg":"pong"}
        - 这是保持连接的唯一心跳机制
        """
        await agent_manager.send_to_agent(self.agent_id, {'msg': 'pong'})

    async def _handle_heartbeat(self, msg: dict) -> None:
        """
        处理心跳消息

        更新 Agent 在线状态和最后心跳时间
        """
        from module_app.agents.entity.do.agents_do import AppAgents
        from sqlalchemy import update

        try:
            # 更新 Agent 状态为在线
            await self.db.execute(
                update(AppAgents)
                .where(AppAgents.id == self.agent_id)
                .values(status=AgentStatusEnum.ONLINE)
            )
            await self.db.commit()
            logger.debug(f'Agent {self.agent_id} 心跳更新成功')
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Agent {self.agent_id} 心跳更新失败: {e}')

    async def _handle_agent_info(self, msg: dict) -> None:
        """
        处理 Agent 信息上报

        保存 Agent 的系统信息、版本等
        """
        from module_app.agents.entity.do.agents_do import AppAgents
        from sqlalchemy import update

        try:
            update_data = {}

            # 提取 Agent 信息
            if 'systemType' in msg:
                update_data['system_type'] = msg['systemType']
            if 'version' in msg:
                update_data['version'] = msg['version']
            if 'highTemp' in msg:
                update_data['high_temp'] = msg['highTemp']
            if 'highTempTime' in msg:
                update_data['high_temp_time'] = msg['highTempTime']

            if update_data:
                await self.db.execute(
                    update(AppAgents)
                    .where(AppAgents.id == self.agent_id)
                    .values(**update_data)
                )
                await self.db.commit()
                logger.info(f'Agent {self.agent_id} 信息已更新: {update_data}')
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Agent {self.agent_id} 信息更新失败: {e}')

    async def _handle_device_detail(self, msg: dict) -> None:
        """
        处理设备详情上报

        更新或创建设备信息
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from module_app.enums import PlatformEnum
        from sqlalchemy import select, update

        ud_id = msg.get('udId')
        detail = msg.get('detail', {})
        platform = msg.get('platform', 1)  # 1=Android, 2=iOS

        if not ud_id:
            logger.warning(f'Agent {self.agent_id} 设备详情缺少 udId')
            return

        try:
            # 查找设备
            result = await self.db.execute(
                select(AppDevices).where(
                    AppDevices.ud_id == ud_id,
                    AppDevices.del_flag == "0"
                )
            )
            device = result.scalars().first()

            device_data = {
                'agent_id': self.agent_id,
                'ud_id': ud_id,
                'name': detail.get('name', ''),
                'model': detail.get('model', ''),
                'manufacturer': detail.get('manufacturer', ''),
                'cpu': detail.get('cpu', ''),
                'size': detail.get('size', ''),
                'version': detail.get('version', ''),
                'platform': PlatformEnum.ANDROID if platform == 1 else PlatformEnum.IOS,
                'status': DeviceStatusEnum.ONLINE,
            }

            # 额外信息
            if 'chiName' in detail:
                device_data['chi_name'] = detail['chiName']
            if 'isHm' in detail:
                device_data['is_hm'] = detail['isHm']

            if device:
                # 更新设备
                await self.db.execute(
                    update(AppDevices)
                    .where(AppDevices.id == device.id)
                    .values(**device_data)
                )
                logger.info(f'设备 {ud_id} 信息已更新')
            else:
                # 创建设备
                new_device = AppDevices(**device_data)
                self.db.add(new_device)
                logger.info(f'设备 {ud_id} 已创建')

            await self.db.commit()

        except Exception as e:
            await self.db.rollback()
            logger.error(f'设备 {ud_id} 详情处理失败: {e}')

    async def _handle_find_steps(self, msg: dict) -> None:
        """
        处理查找步骤请求

        查询用例的所有步骤并返回给 Agent 执行
        这是用例回放的核心功能
        """
        from module_app.websocket.step_finder import StepFinder

        case_id = msg.get('caseId')
        session_id = msg.get('sessionId')
        ud_id = msg.get('udId')
        pwd = msg.get('pwd', '')

        if not case_id:
            logger.warning(f'Agent {self.agent_id} findSteps 缺少 caseId')
            return

        try:
            # 查找步骤
            step_finder = StepFinder(self.db)
            steps_data = await step_finder.find_steps(case_id)

            # 构建响应
            response = {
                'msg': 'runStep',
                'cid': case_id,
                'pf': steps_data.get('pf'),
                'steps': steps_data.get('steps', []),
                'gp': steps_data.get('gp', []),
                'sessionId': session_id,
                'pwd': pwd,
                'udId': ud_id
            }

            await agent_manager.send_to_agent(self.agent_id, response)
            logger.info(f'Agent {self.agent_id} 已发送用例 {case_id} 的步骤')

        except Exception as e:
            logger.error(f'Agent {self.agent_id} 查找步骤失败: {e}')
            # 发送错误响应
            await agent_manager.send_to_agent(self.agent_id, {
                'msg': 'runStep',
                'cid': case_id,
                'error': str(e)
            })

    # ==================== P1 重要消息处理 ====================

    async def _handle_debug_user(self, msg: dict) -> None:
        """
        处理调试用户更新

        更新设备的当前占用者
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from sqlalchemy import update

        ud_id = msg.get('udId')
        user = msg.get('user', '')

        if not ud_id:
            return

        try:
            status = DeviceStatusEnum.DEBUGGING if user else DeviceStatusEnum.ONLINE

            await self.db.execute(
                update(AppDevices)
                .where(AppDevices.ud_id == ud_id, AppDevices.del_flag == "0")
                .values(user=user, status=status)
            )
            await self.db.commit()
            logger.info(f'设备 {ud_id} 调试用户已更新: {user}')

        except Exception as e:
            await self.db.rollback()
            logger.error(f'设备 {ud_id} 调试用户更新失败: {e}')

    async def _handle_battery(self, msg: dict) -> None:
        """
        处理电池信息更新

        更新设备的电量、温度、电压信息
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from sqlalchemy import update

        ud_id = msg.get('udId')
        if not ud_id:
            return

        try:
            update_data = {}
            if 'level' in msg:
                update_data['level'] = msg['level']
            if 'temperature' in msg:
                update_data['temperature'] = msg['temperature']
            if 'voltage' in msg:
                update_data['voltage'] = msg['voltage']

            if update_data:
                await self.db.execute(
                    update(AppDevices)
                    .where(AppDevices.ud_id == ud_id, AppDevices.del_flag == "0")
                    .values(**update_data)
                )
                await self.db.commit()
                logger.debug(f'设备 {ud_id} 电池信息已更新')

        except Exception as e:
            await self.db.rollback()
            logger.error(f'设备 {ud_id} 电池信息更新失败: {e}')

    async def _handle_generate_step(self, msg: dict) -> None:
        """
        处理生成临时步骤请求

        用于元素定位测试，生成一个临时步骤发送给 Agent 执行
        """
        # 直接构建临时步骤响应
        response = {
            'msg': 'runStep',
            'pf': msg.get('pf', 1),
            'steps': [{
                'step': msg.get('stepType', 'click'),
                'elements': msg.get('elements', []),
                'content': msg.get('content', ''),
                'text': msg.get('text', ''),
                'error': 0,
                'conditionType': 0
            }],
            'sessionId': msg.get('sessionId'),
            'udId': msg.get('udId')
        }

        await agent_manager.send_to_agent(self.agent_id, response)
        logger.debug(f'Agent {self.agent_id} 已发送临时步骤')

    async def _handle_error_callback(self, msg: dict) -> None:
        """
        处理错误回调

        记录 Agent 上报的错误信息
        """
        error = msg.get('error', 'Unknown error')
        ud_id = msg.get('udId', '')
        logger.error(f'Agent {self.agent_id} 设备 {ud_id} 错误: {error}')

    # ==================== P2 可选消息处理 ====================

    async def _handle_sub_result_count(self, msg: dict) -> None:
        """
        处理结果计数

        简化处理，仅记录日志
        """
        logger.debug(f'Agent {self.agent_id} 结果计数: {msg}')

    async def _handle_step_result(self, msg: dict) -> None:
        """
        处理步骤执行结果

        记录步骤执行的结果信息
        """
        logger.debug(f'Agent {self.agent_id} 步骤结果: {msg}')

    async def _handle_perform_result(self, msg: dict) -> None:
        """
        处理性能数据

        记录性能测试数据
        """
        logger.debug(f'Agent {self.agent_id} 性能数据: {msg}')

    async def _handle_record(self, msg: dict) -> None:
        """
        处理录制数据

        记录用例录制过程中的数据
        """
        logger.debug(f'Agent {self.agent_id} 录制数据: {msg}')

    async def _handle_status(self, msg: dict) -> None:
        """
        处理状态更新

        记录状态变更信息
        """
        logger.debug(f'Agent {self.agent_id} 状态更新: {msg}')
