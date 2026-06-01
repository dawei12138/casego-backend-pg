from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.module_demo.dao.module_demo_dao import Module_demoDao
from module_admin.module_demo.entity.vo.module_demo_vo import DeleteModule_demoModel, Module_demoModel, Module_demoPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Module_demoService:
    """
    Demo全类型测试模块服务层
    """

    @classmethod
    async def get_module_demo_list_services(
        cls, query_db: AsyncSession, query_object: Module_demoPageQueryModel, is_page: bool = False
    ):
        """
        获取Demo全类型测试列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: Demo全类型测试列表信息对象
        """
        module_demo_list_result = await Module_demoDao.get_module_demo_list(query_db, query_object, is_page)

        return module_demo_list_result


    @classmethod
    async def add_module_demo_services(cls, query_db: AsyncSession, page_object: Module_demoModel):
        """
        新增Demo全类型测试信息service

        :param query_db: orm对象
        :param page_object: 新增Demo全类型测试对象
        :return: 新增Demo全类型测试校验结果
        """
        try:
            await Module_demoDao.add_module_demo_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_module_demo_services(cls, query_db: AsyncSession, page_object: Module_demoModel):
        """
        编辑Demo全类型测试信息service

        :param query_db: orm对象
        :param page_object: 编辑Demo全类型测试对象
        :return: 编辑Demo全类型测试校验结果
        """
        edit_module_demo = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        module_demo_info = await cls.module_demo_detail_services(query_db, page_object.id)
        if module_demo_info.id:
            try:
                await Module_demoDao.edit_module_demo_dao(query_db, edit_module_demo)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='Demo全类型测试不存在')

    @classmethod
    async def delete_module_demo_services(cls, query_db: AsyncSession, page_object: DeleteModule_demoModel):
        """
        删除Demo全类型测试信息service

        :param query_db: orm对象
        :param page_object: 删除Demo全类型测试对象
        :return: 删除Demo全类型测试校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    # id_int = int(id)
                    id_obj = Module_demoModel.model_validate({'id': id}).id
                    # await Module_demoDao.delete_module_demo_dao(query_db, Module_demoModel(id=id_int))
                    await Module_demoDao.delete_module_demo_dao(query_db, Module_demoModel(id=id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID-bigint为空')

    @classmethod
    async def module_demo_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取Demo全类型测试详细信息service

        :param query_db: orm对象
        :param id: 主键ID-bigint
        :return: 主键ID-bigint对应的信息
        """
        module_demo = await Module_demoDao.get_module_demo_detail_by_id(query_db, id=id)
        if module_demo:
            result = Module_demoModel(**CamelCaseUtil.transform_result(module_demo))
        else:
            result = Module_demoModel(**dict())

        return result

    @staticmethod
    async def export_module_demo_list_services(module_demo_list: List):
        """
        导出Demo全类型测试信息service

        :param module_demo_list: Demo全类型测试信息列表
        :return: Demo全类型测试信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID-bigint',
            'stringValue': '字符串-varchar',
            'fixedCharValue': '定长字符-char',
            'unicodeValue': 'Unicode字符串-unicode',
            'textValue': '长文本-text',
            'unicodeTextValue': 'Unicode长文本-unicode text',
            'smallIntegerValue': '短整数-smallint',
            'integerValue': '整数-integer',
            'bigIntegerValue': '长整数-bigint',
            'numericValue': '高精度小数-numeric',
            'decimalValue': '高精度小数-decimal',
            'moneyValue': '金额-money',
            'floatValue': '浮点数-float',
            'realValue': '单精度浮点-real',
            'doubleValue': '双精度浮点-double precision',
            'booleanValue': '布尔-boolean',
            'dateValue': '日期-date',
            'timeValue': '时间-time without time zone',
            'timeTzValue': '带时区时间-time with time zone',
            'datetimeValue': '日期时间-timestamp without time zone',
            'datetimeTzValue': '带时区日期时间-timestamp with time zone',
            'intervalValue': '时间间隔-interval',
            'jsonValue': 'JSON-json',
            'jsonbObjectValue': 'JSON对象-jsonb/object',
            'jsonbArrayValue': 'JSON数组-jsonb/array',
            'jsonpathValue': 'JSON路径-jsonpath',
            'binaryValue': '二进制-bytea',
            'enumValue': '枚举-enum',
            'uuidValue': 'UUID-uuid',
            'stringArrayValue': '字符串数组-array/varchar',
            'integerArrayValue': '整数数组-array/integer',
            'jsonbArrayItemsValue': 'JSONB数组-array/jsonb',
            'inetValue': 'IP地址-inet',
            'cidrValue': '网络地址-cidr',
            'macaddrValue': 'MAC地址-macaddr',
            'macaddr8Value': 'EUI-64 MAC地址-macaddr8',
            'bitValue': '固定长度位-bit',
            'bitVaryingValue': '可变长度位-bit varying',
            'tsvectorValue': '全文检索向量-tsvector',
            'tsqueryValue': '全文检索查询-tsquery',
            'int4RangeValue': '整数范围-int4range',
            'int8RangeValue': '长整数范围-int8range',
            'numericRangeValue': '小数范围-numrange',
            'dateRangeValue': '日期范围-daterange',
            'timestampRangeValue': '时间戳范围-tsrange',
            'timestampTzRangeValue': '带时区时间戳范围-tstzrange',
            'int4MultirangeValue': '整数多范围-int4multirange',
            'int8MultirangeValue': '长整数多范围-int8multirange',
            'numericMultirangeValue': '小数多范围-nummultirange',
            'dateMultirangeValue': '日期多范围-datemultirange',
            'timestampMultirangeValue': '时间戳多范围-tsmultirange',
            'timestampTzMultirangeValue': '带时区时间戳多范围-tstzmultirange',
            'oidValue': '对象ID-oid',
            'regclassValue': '关系对象-regclass',
            'regconfigValue': '文本搜索配置-regconfig',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'sortNo': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(module_demo_list, mapping_dict)

        return binary_data
