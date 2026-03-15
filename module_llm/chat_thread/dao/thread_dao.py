from sqlalchemy import delete, select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_llm.chat_thread.entity.do.thread_do import LlmChatThread
from module_llm.chat_thread.entity.vo.thread_vo import ThreadModel, ThreadPageQueryModel, ThreadQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db


class ThreadDao:
    """
    LLM聊天线程模块数据库操作层
    """

    @classmethod
    async def get_thread_detail_by_id(cls, db: AsyncSession, thread_id: int):
        """
        根据线程唯一标识符(UUID格式)获取LLM聊天线程详细信息

        :param db: orm对象
        :param thread_id: 线程唯一标识符(UUID格式)
        :return: LLM聊天线程信息对象
        """
        thread_info = (
            (
                await db.execute(
                    select(LlmChatThread)
                    .where(
                        LlmChatThread.thread_id == thread_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return thread_info

    @classmethod
    async def get_thread_detail_by_info(cls, db: AsyncSession, thread: ThreadModel):
        """
        根据LLM聊天线程参数获取LLM聊天线程信息

        :param db: orm对象
        :param thread: LLM聊天线程参数对象
        :return: LLM聊天线程信息对象
        """
        thread_info = (
            (
                await db.execute(
                    select(LlmChatThread).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return thread_info

    @classmethod
    async def get_thread_list(cls, db: AsyncSession, query_object: ThreadPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取LLM聊天线程列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: LLM聊天线程列表信息字典对象
        """
        query = (
            select(LlmChatThread)
            .where(
                LlmChatThread.title == query_object.title if query_object.title else True,
                LlmChatThread.user_id == query_object.user_id if query_object.user_id else True,
            )
            .where(LlmChatThread.del_flag == "0")
            .order_by(desc(LlmChatThread.create_time))
            # .distinct()
        )
        thread_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return thread_list

    @classmethod
    async def get_thread_orm_list(cls, db: AsyncSession, query_object: ThreadQueryModel) -> List[ThreadQueryModel]:
        """
        根据查询参数获取LLM聊天线程列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: LLM聊天线程列表信息orm对象
        """
        query = (
            select(LlmChatThread)
            .where(
                LlmChatThread.title == query_object.title if query_object.title else True,
                LlmChatThread.user_id == query_object.user_id if query_object.user_id else True,
            )
            .where(LlmChatThread.del_flag == "0")
            .order_by(desc(LlmChatThread.create_time))
            # .distinct()
        )

        result = await db.execute(query)
        return [ThreadQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_thread_dao(cls, db: AsyncSession, thread: ThreadModel):
        """
        新增LLM聊天线程数据库操作

        :param db: orm对象
        :param thread: LLM聊天线程对象
        :return:
        """
        db_thread = LlmChatThread(**thread.model_dump(exclude={}))
        db.add(db_thread)
        await db.flush()

        return db_thread

    @classmethod
    async def edit_thread_dao(cls, db: AsyncSession, thread: dict):
        """
        编辑LLM聊天线程数据库操作

        :param db: orm对象
        :param thread: 需要更新的LLM聊天线程字典
        :return:
        """
        await db.execute(update(LlmChatThread), [thread])

    @classmethod
    async def delete_thread_dao(cls, db: AsyncSession, thread: ThreadModel):
        """
        删除LLM聊天线程数据库操作

        :param db: orm对象
        :param thread: LLM聊天线程对象
        :return:
        """
        # await db.execute(delete(LlmChatThread).where(LlmChatThread.thread_id.in_([thread.thread_id])))
        await db.execute(
            update(LlmChatThread).where(LlmChatThread.thread_id.in_([thread.thread_id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = ThreadPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await ThreadDao.get_thread_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
