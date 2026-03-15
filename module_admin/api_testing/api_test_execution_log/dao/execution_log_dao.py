from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from module_admin.api_testing.api_test_execution_log.entity.do.execution_log_do import ApiTestExecutionLog
from module_admin.api_testing.api_test_execution_log.entity.vo.execution_log_vo import Execution_logModel, \
    Execution_logPageQueryModel, Execution_logQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db


class Execution_logDao:
    """
    接口测试执行日志模块数据库操作层
    """

    @classmethod
    async def get_execution_log_detail_by_id(cls, db: AsyncSession, log_id: int):
        """
        根据执行日志ID获取接口测试执行日志详细信息

        :param db: orm对象
        :param log_id: 执行日志ID
        :return: 接口测试执行日志信息对象
        """
        execution_log_info = (
            (
                await db.execute(
                    select(ApiTestExecutionLog)
                    .where(
                        ApiTestExecutionLog.log_id == log_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return execution_log_info

    @classmethod
    async def get_execution_log_detail_by_info(cls, db: AsyncSession, execution_log: Execution_logModel):
        """
        根据接口测试执行日志参数获取接口测试执行日志信息

        :param db: orm对象
        :param execution_log: 接口测试执行日志参数对象
        :return: 接口测试执行日志信息对象
        """
        execution_log_info = (
            (
                await db.execute(
                    select(ApiTestExecutionLog).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return execution_log_info

    @classmethod
    async def get_execution_log_list(cls, db: AsyncSession, query_object: Execution_logPageQueryModel,
                                     is_page: bool = False):
        """
        根据查询参数获取接口测试执行日志列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口测试执行日志列表信息字典对象
        """
        # 定义要选择的字段（排除 execution_data）
        # selected_columns = [
        #     ApiTestExecutionLog.log_id,
        #     ApiTestExecutionLog.case_id,
        #     ApiTestExecutionLog.execution_time,
        #     ApiTestExecutionLog.is_success,
        #     # ApiTestExecutionLog.execution_data,  # 排除这个字段
        #     ApiTestExecutionLog.response_status_code,
        #     ApiTestExecutionLog.response_time,
        #     ApiTestExecutionLog.assertion_success,
        #     ApiTestExecutionLog.description,
        #     ApiTestExecutionLog.sort_no,
        #     ApiTestExecutionLog.del_flag,
        #     # 添加其他你需要的字段...
        # ]

        query = (
            select(ApiTestExecutionLog)
            .options(defer(ApiTestExecutionLog.execution_data))  # 排除这个字段
            .where(
                ApiTestExecutionLog.case_id == query_object.case_id if query_object.case_id else True,
                ApiTestExecutionLog.execution_time == query_object.execution_time if query_object.execution_time else True,
                ApiTestExecutionLog.is_success == query_object.is_success if query_object.is_success else True,
                # 移除 execution_data 的查询条件，因为不再选择这个字段
                # ApiTestExecutionLog.execution_data == query_object.execution_data if query_object.execution_data else True,
                ApiTestExecutionLog.response_status_code == query_object.response_status_code if query_object.response_status_code else True,
                ApiTestExecutionLog.response_time == query_object.response_time if query_object.response_time else True,
                ApiTestExecutionLog.assertion_success == query_object.assertion_success if query_object.assertion_success else True,
                ApiTestExecutionLog.description == query_object.description if query_object.description else True,
                ApiTestExecutionLog.sort_no == query_object.sort_no if query_object.sort_no else True,
                ApiTestExecutionLog.report_id == query_object.report_id if query_object.report_id else True,
            )
            .where(ApiTestExecutionLog.del_flag == "0")
            .order_by(ApiTestExecutionLog.execution_time.desc())
            #.distinct()
        )
        execution_log_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return execution_log_list

    @classmethod
    async def get_execution_log_orm_list(cls, db: AsyncSession, query_object: Execution_logQueryModel):
        """
        根据查询参数获取接口测试执行日志列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口测试执行日志列表信息orm对象
        """
        query = (
            select(ApiTestExecutionLog)
            .options(defer(ApiTestExecutionLog.execution_data))  # 排除这个字段
            .where(
                ApiTestExecutionLog.case_id == query_object.case_id if query_object.case_id else True,
                ApiTestExecutionLog.execution_time == query_object.execution_time if query_object.execution_time else True,
                ApiTestExecutionLog.is_success == query_object.is_success if query_object.is_success else True,
                # ApiTestExecutionLog.execution_data == query_object.execution_data if query_object.execution_data else True,
                ApiTestExecutionLog.response_status_code == query_object.response_status_code if query_object.response_status_code else True,
                ApiTestExecutionLog.response_time == query_object.response_time if query_object.response_time else True,
                ApiTestExecutionLog.assertion_success == query_object.assertion_success if query_object.assertion_success else True,
                ApiTestExecutionLog.description == query_object.description if query_object.description else True,
                ApiTestExecutionLog.sort_no == query_object.sort_no if query_object.sort_no else True,
                ApiTestExecutionLog.report_id == query_object.report_id if query_object.report_id else True,
            )
            .where(ApiTestExecutionLog.del_flag == "0")
            .order_by(ApiTestExecutionLog.sort_no)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_execution_log_dao(cls, db: AsyncSession, execution_log: Execution_logModel):
        """
        新增接口测试执行日志数据库操作

        :param db: orm对象
        :param execution_log: 接口测试执行日志对象
        :return:
        """
        db_execution_log = ApiTestExecutionLog(**execution_log.model_dump(exclude={}))
        db.add(db_execution_log)
        await db.flush()

        return db_execution_log

    @classmethod
    async def edit_execution_log_dao(cls, db: AsyncSession, execution_log: dict):
        """
        编辑接口测试执行日志数据库操作

        :param db: orm对象
        :param execution_log: 需要更新的接口测试执行日志字典
        :return:
        """
        await db.execute(update(ApiTestExecutionLog), [execution_log])

    @classmethod
    async def delete_execution_log_dao(cls, db: AsyncSession, execution_log: Execution_logModel):
        """
        删除接口测试执行日志数据库操作

        :param db: orm对象
        :param execution_log: 接口测试执行日志对象
        :return:
        """
        # await db.execute(delete(ApiTestExecutionLog).where(ApiTestExecutionLog.log_id.in_([execution_log.log_id])))
        await db.execute(
            update(ApiTestExecutionLog).where(ApiTestExecutionLog.log_id.in_([execution_log.log_id])).values(
                del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Execution_logPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Execution_logDao.get_execution_log_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
