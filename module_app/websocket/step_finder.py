# -*- coding: utf-8 -*-
"""
步骤查找器

负责查询测试用例的所有步骤、关联元素和全局参数
对应 Phase 3.1.1 核心方法: find_steps()
"""
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils.log_util import logger


class StepFinder:
    """
    步骤查找器

    查询用例的完整步骤信息，包括关联的元素和全局参数
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_steps(self, case_id: int) -> Dict:
        """
        查找用例的所有步骤，包含元素信息

        :param case_id: 用例ID
        :return: 包含步骤、元素、全局参数的字典

        返回格式:
        {
            "pf": platform,  # 平台类型 (1=Android, 2=iOS)
            "steps": [
                {
                    "id": 1,
                    "stepType": "click",
                    "content": "",
                    "text": "",
                    "elements": [
                        {
                            "id": 1,
                            "eleName": "登录按钮",
                            "eleType": "id",
                            "eleValue": "com.example:id/login"
                        }
                    ],
                    "error": 0,
                    "conditionType": 0,
                    "disabled": 0
                }
            ],
            "gp": [
                {
                    "paramsKey": "username",
                    "paramsValue": "testuser"
                }
            ]
        }
        """
        from module_app.cases.entity.do.cases_do import AppTestCases
        from module_app.steps.entity.do.steps_do import AppSteps
        from module_app.steps_elements.entity.do.steps_elements_do import AppStepsElements
        from module_app.elements.entity.do.elements_do import AppElements
        from module_app.globalparams.entity.do.globalparams_do import AppGlobalParams

        try:
            # 1. 查询用例信息
            result = await self.db.execute(
                select(AppTestCases).where(AppTestCases.id == case_id)
            )
            test_case = result.scalars().first()

            if not test_case:
                logger.error(f'用例不存在: case_id={case_id}')
                raise ValueError(f'测试用例 {case_id} 不存在')

            platform = test_case.platform.value  # 转换枚举为整数值
            project_id = test_case.project_id

            # 2. 查询用例的所有步骤（按sort排序，如果有sort字段）
            steps_result = await self.db.execute(
                select(AppSteps)
                .where(AppSteps.case_id == case_id)
                .order_by(AppSteps.id)  # 暂时按ID排序，等sort字段添加后改为sort
            )
            steps = steps_result.scalars().all()

            # 3. 组装步骤数据
            steps_data = []
            for step in steps:
                # 3.1 查询步骤关联的元素
                elements_result = await self.db.execute(
                    select(AppElements)
                    .join(
                        AppStepsElements,
                        AppStepsElements.elements_id == AppElements.id
                    )
                    .where(AppStepsElements.steps_id == step.id)
                )
                elements = elements_result.scalars().all()

                # 3.2 组装元素数据
                elements_data = []
                for element in elements:
                    elements_data.append({
                        'id': element.id,
                        'eleName': element.ele_name or '',
                        'eleType': element.ele_type.value if element.ele_type else '',
                        'eleValue': element.ele_value or ''
                    })

                # 3.3 组装步骤数据
                step_dict = {
                    'id': step.id,
                    'stepType': step.step_type or '',
                    'content': step.content or '',
                    'text': step.text or '',
                    'elements': elements_data,
                    'error': step.error.value if step.error else 0,
                    'conditionType': step.condition_type.value if step.condition_type else 0,
                    'disabled': step.disabled.value if step.disabled else 0
                }

                steps_data.append(step_dict)

            # 4. 查询全局参数
            gp_result = await self.db.execute(
                select(AppGlobalParams)
                .where(AppGlobalParams.project_id == project_id)
            )
            global_params = gp_result.scalars().all()

            # 4.1 组装全局参数数据
            gp_data = []
            for gp in global_params:
                gp_data.append({
                    'paramsKey': gp.params_key or '',
                    'paramsValue': gp.params_value or ''
                })

            # 5. 返回完整数据
            result_data = {
                'pf': platform,
                'steps': steps_data,
                'gp': gp_data
            }

            logger.info(
                f'成功查找用例步骤: case_id={case_id}, '
                f'步骤数={len(steps_data)}, 全局参数数={len(gp_data)}'
            )

            return result_data

        except Exception as e:
            logger.error(f'查找用例步骤失败: case_id={case_id}, error={e}')
            raise
