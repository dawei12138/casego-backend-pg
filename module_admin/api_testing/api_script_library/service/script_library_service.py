from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_script_library.dao.script_library_dao import Script_libraryDao
from module_admin.api_testing.api_script_library.entity.vo.script_library_vo import DeleteScript_libraryModel, Script_libraryModel, Script_libraryPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Script_libraryService:
    """
    公共脚本库模块服务层
    """

    @classmethod
    async def get_script_library_list_services(
        cls, query_db: AsyncSession, query_object: Script_libraryPageQueryModel, is_page: bool = False
    ):
        """
        获取公共脚本库列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公共脚本库列表信息对象
        """
        script_library_list_result = await Script_libraryDao.get_script_library_list(query_db, query_object, is_page)

        return script_library_list_result


    @classmethod
    async def add_script_library_services(cls, query_db: AsyncSession, page_object: Script_libraryModel):
        """
        新增公共脚本库信息service

        :param query_db: orm对象
        :param page_object: 新增公共脚本库对象
        :return: 新增公共脚本库校验结果
        """
        try:
            await Script_libraryDao.add_script_library_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_script_library_services(cls, query_db: AsyncSession, page_object: Script_libraryModel):
        """
        编辑公共脚本库信息service

        :param query_db: orm对象
        :param page_object: 编辑公共脚本库对象
        :return: 编辑公共脚本库校验结果
        """
        edit_script_library = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'remark', 'description', 'sort_no', 'del_flag'})
        script_library_info = await cls.script_library_detail_services(query_db, page_object.script_id)
        if script_library_info.script_id:
            try:
                await Script_libraryDao.edit_script_library_dao(query_db, edit_script_library)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='公共脚本库不存在')

    @classmethod
    async def delete_script_library_services(cls, query_db: AsyncSession, page_object: DeleteScript_libraryModel):
        """
        删除公共脚本库信息service

        :param query_db: orm对象
        :param page_object: 删除公共脚本库对象
        :return: 删除公共脚本库校验结果
        """
        if page_object.script_ids:
            script_id_list = page_object.script_ids.split(',')
            try:
                for script_id in script_id_list:
                    await Script_libraryDao.delete_script_library_dao(query_db, Script_libraryModel(scriptId=script_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入脚本ID为空')

    @classmethod
    async def script_library_detail_services(cls, query_db: AsyncSession, script_id: int):
        """
        获取公共脚本库详细信息service

        :param query_db: orm对象
        :param script_id: 脚本ID
        :return: 脚本ID对应的信息
        """
        script_library = await Script_libraryDao.get_script_library_detail_by_id(query_db, script_id=script_id)
        if script_library:
            result = Script_libraryModel(**CamelCaseUtil.transform_result(script_library))
        else:
            result = Script_libraryModel(**dict())

        return result

    @staticmethod
    async def export_script_library_list_services(script_library_list: List):
        """
        导出公共脚本库信息service

        :param script_library_list: 公共脚本库信息列表
        :return: 公共脚本库信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'scriptId': '脚本ID',
            'scriptName': '脚本名称',
            'scriptType': '脚本类型(python/javascript)',
            'scriptContent': '脚本内容',
            'status': '状态(0停用 1正常)',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(script_library_list, mapping_dict)

        return binary_data
