from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_llm.chat_thread.dao.thread_dao import ThreadDao
from module_llm.chat_thread.entity.vo.thread_vo import DeleteThreadModel, ThreadModel, ThreadPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ThreadService:
    """
    LLM聊天线程模块服务层
    """

    @classmethod
    async def get_thread_list_services(
            cls, query_db: AsyncSession, query_object: ThreadPageQueryModel, is_page: bool = False
    ):
        """
        获取LLM聊天线程列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: LLM聊天线程列表信息对象
        """
        thread_list_result = await ThreadDao.get_thread_list(query_db, query_object, is_page)

        return thread_list_result

    @classmethod
    async def add_thread_services(cls, query_db: AsyncSession, page_object: ThreadModel):
        """
        新增LLM聊天线程信息service

        :param query_db: orm对象
        :param page_object: 新增LLM聊天线程对象
        :return: 新增LLM聊天线程校验结果
        """
        try:
            await ThreadDao.add_thread_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_thread_services(cls, query_db: AsyncSession, page_object: ThreadModel):
        """
        编辑LLM聊天线程信息service

        :param query_db: orm对象
        :param page_object: 编辑LLM聊天线程对象
        :return: 编辑LLM聊天线程校验结果
        """
        edit_thread = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        thread_info = await cls.thread_detail_services(query_db, page_object.thread_id)
        if thread_info.thread_id:
            try:
                await ThreadDao.edit_thread_dao(query_db, edit_thread)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='LLM聊天线程不存在')

    @classmethod
    async def delete_thread_services(cls, query_db: AsyncSession, page_object: DeleteThreadModel):
        """
        删除LLM聊天线程信息service

        :param query_db: orm对象
        :param page_object: 删除LLM聊天线程对象
        :return: 删除LLM聊天线程校验结果
        """
        if page_object.thread_ids:
            thread_id_list = page_object.thread_ids.split(',')
            try:
                for thread_id in thread_id_list:
                    # thread_id_int = int(thread_id)
                    thread_id_obj = ThreadModel.model_validate({'thread_id': thread_id}).thread_id
                    # await ThreadDao.delete_thread_dao(query_db, ThreadModel(threadId=thread_id_int))
                    await ThreadDao.delete_thread_dao(query_db, ThreadModel(threadId=thread_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入线程唯一标识符(UUID格式)为空')

    @classmethod
    async def thread_detail_services(cls, query_db: AsyncSession, thread_id: int):
        """
        获取LLM聊天线程详细信息service

        :param query_db: orm对象
        :param thread_id: 线程唯一标识符(UUID格式)
        :return: 线程唯一标识符(UUID格式)对应的信息
        """
        thread = await ThreadDao.get_thread_detail_by_id(query_db, thread_id=thread_id)
        if thread:
            result = ThreadModel(**CamelCaseUtil.transform_result(thread))
        else:
            result = ThreadModel(**dict())

        return result

    @staticmethod
    async def export_thread_list_services(thread_list: List):
        """
        导出LLM聊天线程信息service

        :param thread_list: LLM聊天线程信息列表
        :return: LLM聊天线程信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'threadId': '线程唯一标识符(UUID格式)',
            'title': '线程标题，首次对话后自动生成',
            'userId': '所属用户ID',
            'sessionConfig': '会话配置(JSON格式)，如temperature、max_tokens、system_prompt等',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(thread_list, mapping_dict)

        return binary_data
