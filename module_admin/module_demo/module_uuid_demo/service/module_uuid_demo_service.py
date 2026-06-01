from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.module_demo.module_uuid_demo.dao.module_uuid_demo_dao import Module_uuid_demoDao
from module_admin.module_demo.module_uuid_demo.entity.vo.module_uuid_demo_vo import DeleteModule_uuid_demoModel, Module_uuid_demoModel, Module_uuid_demoPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Module_uuid_demoService:
    """
    UUID主键业务示例模块服务层
    """

    @classmethod
    async def get_module_uuid_demo_list_services(
        cls, query_db: AsyncSession, query_object: Module_uuid_demoPageQueryModel, is_page: bool = False
    ):
        """
        获取UUID主键业务示例列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: UUID主键业务示例列表信息对象
        """
        module_uuid_demo_list_result = await Module_uuid_demoDao.get_module_uuid_demo_list(query_db, query_object, is_page)

        return module_uuid_demo_list_result


    @classmethod
    async def add_module_uuid_demo_services(cls, query_db: AsyncSession, page_object: Module_uuid_demoModel):
        """
        新增UUID主键业务示例信息service

        :param query_db: orm对象
        :param page_object: 新增UUID主键业务示例对象
        :return: 新增UUID主键业务示例校验结果
        """
        page_object = Module_uuid_demoModel.model_validate(page_object.model_dump())
        try:
            await Module_uuid_demoDao.add_module_uuid_demo_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_module_uuid_demo_services(cls, query_db: AsyncSession, page_object: Module_uuid_demoModel):
        """
        编辑UUID主键业务示例信息service

        :param query_db: orm对象
        :param page_object: 编辑UUID主键业务示例对象
        :return: 编辑UUID主键业务示例校验结果
        """
        page_object = Module_uuid_demoModel.model_validate(page_object.model_dump())
        edit_module_uuid_demo = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag', })
        module_uuid_demo_info = await cls.module_uuid_demo_detail_services(query_db, page_object.id)
        if module_uuid_demo_info.id:
            try:
                await Module_uuid_demoDao.edit_module_uuid_demo_dao(query_db, edit_module_uuid_demo)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='UUID主键业务示例不存在')

    @classmethod
    async def delete_module_uuid_demo_services(cls, query_db: AsyncSession, page_object: DeleteModule_uuid_demoModel):
        """
        删除UUID主键业务示例信息service

        :param query_db: orm对象
        :param page_object: 删除UUID主键业务示例对象
        :return: 删除UUID主键业务示例校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id_obj = Module_uuid_demoModel.model_validate({'id': id}).id
                    await Module_uuid_demoDao.delete_module_uuid_demo_dao(query_db, Module_uuid_demoModel(id=id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID-uuid为空')

    @classmethod
    async def module_uuid_demo_detail_services(cls, query_db: AsyncSession, id: str):
        """
        获取UUID主键业务示例详细信息service

        :param query_db: orm对象
        :param id: 主键ID-uuid
        :return: 主键ID-uuid对应的信息
        """
        module_uuid_demo = await Module_uuid_demoDao.get_module_uuid_demo_detail_by_id(query_db, id=id)
        if module_uuid_demo:
            result = Module_uuid_demoModel(**CamelCaseUtil.transform_result(module_uuid_demo))
        else:
            result = Module_uuid_demoModel(**dict())

        return result

    @staticmethod
    async def export_module_uuid_demo_list_services(module_uuid_demo_list: List):
        """
        导出UUID主键业务示例信息service

        :param module_uuid_demo_list: UUID主键业务示例信息列表
        :return: UUID主键业务示例信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID-uuid',
            'title': '业务标题',
            'businessCode': '业务编号',
            'customerName': '客户名称',
            'status': '业务状态',
            'priority': '优先级',
            'amount': '业务金额',
            'enabled': '是否启用',
            'occurredDate': '发生日期',
            'closedTime': '关闭时间',
            'extraInfo': '扩展信息',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序号',
            'delFlag': '删除标志',
            'type': '业务类型',
        }
        binary_data = ExcelUtil.export_list2excel(module_uuid_demo_list, mapping_dict)

        return binary_data
