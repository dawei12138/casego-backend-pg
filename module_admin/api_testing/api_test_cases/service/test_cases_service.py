from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.api_project_submodules.entity.vo.project_submodules_vo import Project_submodulesPageQueryModel, \
    Project_submodulesModel
from module_admin.api_project_submodules.service.project_submodules_service import Project_submodulesService
from module_admin.api_testing.api_assertions.entity.do.assertions_do import ApiAssertions
from module_admin.api_testing.api_cookies.entity.do.cookies_do import ApiCookies
from module_admin.api_testing.api_formdata.entity.do.formdata_do import ApiFormdata
from module_admin.api_testing.api_headers.entity.do.headers_do import ApiHeaders
from module_admin.api_testing.api_params.entity.do.params_do import ApiParams
from module_admin.api_testing.api_setup.entity.do.setup_do import ApiSetup
from module_admin.api_testing.api_teardown.entity.do.teardown_do import ApiTeardown
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.service.dict_service import DictDataService
from module_admin.api_testing.api_test_cases.dao.test_cases_dao import Test_casesDao
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import DeleteTest_casesModel, Test_casesModel, \
    Test_casesPageQueryModel, Test_casesAllParamsQueryModel
from utils.excel_util import ExcelUtil


class Test_casesService:
    """
    接口用例模块服务层
    """

    @classmethod
    async def get_test_cases_list_services(
            cls, query_db: AsyncSession, query_object: Test_casesPageQueryModel, is_page: bool = False
    ):
        """
        获取接口用例列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口用例列表信息对象
        """
        test_cases_list_result = await Test_casesDao.get_test_cases_list(query_db, query_object, is_page)

        return test_cases_list_result

    @classmethod
    async def add_test_cases_services(cls, query_db: AsyncSession, page_object: Test_casesModel):
        """
        新增接口用例信息service

        :param query_db: orm对象
        :param page_object: 新增接口用例对象
        :return: 新增接口用例校验结果
        """
        try:
            # if page_object.parent_submodule_id:
            new_case = await Test_casesDao.add_test_cases_dao(query_db, page_object)
            await query_db.commit()
            await query_db.refresh(new_case)  # 显式刷新对象以获取数据库生成的值
            return {"caseId": new_case.case_id}
            # else:
            #     submodules_query_object = Project_submodulesPageQueryModel(
            #         name="快速创建",
            #         project_id=page_object.project_id,
            #         type="1"
            #     )
            #     res_submodules = await Project_submodulesService.get_project_submodules_list_services(query_db,
            #                                                                                           submodules_query_object)
            #     if len(res_submodules) != 0:
            #         module_id = res_submodules[0].get("id")
            #     else:
            #         res_module = await Project_submodulesService.add_project_submodules_services(query_db,
            #                                                                                      Project_submodulesModel(
            #                                                                                          name="快速创建",
            #                                                                                          project_id=page_object.project_id,
            #                                                                                          type="1"), )
            #         module_id = res_module.get("moduleId")
            #     page_object.parent_submodule_id = module_id
            #     new_case = await Test_casesDao.add_test_cases_dao(query_db, page_object)
            #     await query_db.commit()
            #     await query_db.refresh(new_case)  # 显式刷新对象以获取数据库生成的值
            #     return {"caseId": new_case.case_id}

        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_test_cases_services(cls, query_db: AsyncSession, page_object: Test_casesAllParamsQueryModel):
        """
        编辑接口用例信息service

        :param query_db: orm对象
        :param page_object: 编辑接口用例对象
        :return: 编辑接口用例校验结果
        """
        for i in page_object.cookies_list:
            i.case_id = page_object.case_id
        for i in page_object.headers_list:
            i.case_id = page_object.case_id
        for i in page_object.params_list:
            i.case_id = page_object.case_id
        for i in page_object.setup_list:
            i.case_id = page_object.case_id
        for i in page_object.teardown_list:
            i.case_id = page_object.case_id
        for i in page_object.assertion_list:
            i.case_id = page_object.case_id
        for i in page_object.formdata:
            i.case_id = page_object.case_id

        edit_test_cases = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        test_cases_info = await cls.test_cases_detail_services(query_db, page_object.case_id)
        if test_cases_info.case_id:
            try:
                await Test_casesDao.edit_test_cases_dao(query_db, edit_test_cases)
                [await query_db.merge(
                    (ApiHeaders(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                                update_by=page_object.update_by,
                                update_time=page_object.update_time))) for
                 data_model in page_object.headers_list]
                [await query_db.merge(
                    (ApiCookies(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                                update_by=page_object.update_by,
                                update_time=page_object.update_time))) for
                 data_model in page_object.cookies_list]
                [await query_db.merge(
                    (ApiParams(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                               update_by=page_object.update_by,
                               update_time=page_object.update_time))) for
                 data_model in page_object.params_list]
                [await query_db.merge(
                    (ApiAssertions(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                                   update_by=page_object.update_by,
                                   update_time=page_object.update_time))) for
                 data_model in page_object.assertion_list]
                [await query_db.merge(
                    (ApiSetup(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                              update_by=page_object.update_by,
                              update_time=page_object.update_time))) for
                 data_model in page_object.setup_list]
                [await query_db.merge(
                    (ApiTeardown(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                                 update_by=page_object.update_by,
                                 update_time=page_object.update_time))) for
                 data_model in page_object.teardown_list]
                [await query_db.merge(
                    (ApiFormdata(**data_model.model_dump(exclude_unset=True, exclude={'update_by', 'update_time', }),
                                 update_by=page_object.update_by,
                                 update_time=page_object.update_time))) for
                 data_model in page_object.formdata]

                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口用例不存在')

    @classmethod
    async def delete_test_cases_services(cls, query_db: AsyncSession, page_object: DeleteTest_casesModel):
        """
        删除接口用例信息service

        :param query_db: orm对象
        :param page_object: 删除接口用例对象
        :return: 删除接口用例校验结果
        """
        if page_object.case_ids:
            case_id_list = page_object.case_ids.split(',')
            try:
                for case_id in case_id_list:
                    await Test_casesDao.delete_test_cases_dao(query_db, Test_casesModel(caseId=case_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入测试用例ID为空')

    @classmethod
    async def test_cases_detail_services(cls, query_db: AsyncSession, case_id: int) -> Test_casesAllParamsQueryModel:
        """
        获取接口用例详细信息service

        :param query_db: orm对象
        :param case_id: 测试用例ID
        :return: 测试用例ID对应的信息
        """
        # test_cases = await Test_casesDao.get_test_cases_detail_by_id(query_db, case_id=case_id)
        test_cases = await Test_casesDao.get_test_cases_all_detail_by_id(query_db, case_id=case_id)
        if test_cases:
            # result = Test_casesModel(**CamelCaseUtil.transform_result(test_cases))
            result = test_cases
        else:
            result = Test_casesAllParamsQueryModel(**dict())

        return result

    @classmethod
    async def test_cases_copy_services(cls, query_db: AsyncSession, page_query: Test_casesModel, is_copy_to_case=False,
                                       is_copy_to_workflownode_case=False):
        """
        直接复制接口：
        :param query_db: orm对象
        :param page_query: 包含要复制的case_id和其他更新信息
        :return: 复制结束的新case_id，失败返回None
        """
        exclude = {
            "case_id", "cookies_list", "headers_list", "params_list",
            "setup_list", "teardown_list", "assertion_list", "formdata"
        }

        try:
            # 获取被复制用例信息
            test_cases = await Test_casesDao.get_test_cases_all_detail_by_id(
                query_db, case_id=page_query.case_id
            )

            if not test_cases:
                return None

            # 创建新的测试用例基础信息
            test_info = Test_casesModel(**test_cases.model_dump(exclude_unset=True, exclude=exclude))
            test_info = test_info.model_copy(update=page_query.model_dump(
                exclude_unset=True,
                include={"create_by", "create_time", "update_by", "update_time"}
            ))

            # 转化成用例需要额外参数
            if is_copy_to_case:
                test_info.case_type = "2"
                test_info.copy_id = page_query.case_id
                test_info.parent_case_id = page_query.case_id
                test_info.name = page_query.name
            # 此为工作流节点复制的用例
            elif is_copy_to_workflownode_case:
                test_info.case_type = "3"
                test_info.copy_id = page_query.case_id
                # test_info.parent_case_id = page_query.case_id
                # test_info.name = page_query.name
            else:
                test_info.name = test_info.name + "_copy"
            # 添加新的测试用例
            db_test_cases = await Test_casesDao.add_test_cases_dao(query_db, test_info)
            new_case_id = db_test_cases.case_id
            new_case_name = db_test_cases.name

            # 定义每个模型类对应的主键字段名
            model_primary_keys = {
                ApiHeaders: "header_id",
                ApiCookies: "cookie_id",
                ApiParams: "param_id",
                ApiAssertions: "assertion_id",
                ApiSetup: "setup_id",
                ApiTeardown: "teardown_id",
                ApiFormdata: "formdata_id"
            }

            async def copy_related_data(data_list, model_class):
                """复制关联数据的通用方法"""
                if not data_list:
                    return

                primary_key = model_primary_keys.get(model_class, "id")

                for data_model in data_list:
                    # 创建新的数据模型，排除主键，设置新的case_id
                    new_data = data_model.model_dump(exclude_unset=True, exclude={primary_key})
                    new_data["case_id"] = new_case_id
                    new_data["create_by"] = page_query.create_by
                    new_data["create_time"] = page_query.create_time
                    new_data["update_by"] = page_query.update_by
                    new_data["update_time"] = page_query.update_time
                    new_instance = model_class(**new_data)
                    query_db.add(new_instance)

            # 复制所有关联数据
            await copy_related_data(test_cases.headers_list, ApiHeaders)
            await copy_related_data(test_cases.cookies_list, ApiCookies)
            await copy_related_data(test_cases.params_list, ApiParams)
            await copy_related_data(test_cases.assertion_list, ApiAssertions)
            await copy_related_data(test_cases.setup_list, ApiSetup)
            await copy_related_data(test_cases.teardown_list, ApiTeardown)
            await copy_related_data(test_cases.formdata, ApiFormdata)

            # 提交事务
            await query_db.commit()

            return {"caseId": new_case_id, "caseName": new_case_name}

        except Exception as e:
            await query_db.rollback()
            # 记录错误日志
            print(f"复制测试用例失败: {str(e)}")
            return None

    @staticmethod
    async def export_test_cases_list_services(request: Request, test_cases_list: List):
        """
        导出接口用例信息service

        :param request:
        :param test_cases_list: 接口用例信息列表
        :return: 接口用例信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'caseId': '测试用例ID',
            'name': '测试用例名称',
            'caseType': '测试用例类型 (1接口, 2用例等)',
            'copyId': '复制过来的接口用例ID',
            'parentCaseId': '父级测试接口ID',
            'parentSubmoduleId': '父级模块ID',
            'description': '测试接口/用例描述',
            'path': '请求路径',
            'method': '请求方法 (GET, POST等)',
            'requestType': '请求类型 (1-None,2-Form Data,3-x-www-form-urlencoded,4-JSON, 5-xml,6-Raw,7-Binary,8-File)',
            'isRun': '是否执行',
            'statusCode': '预期状态码',
            'sleep': '执行前等待时间 (毫秒)',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
            'data': '请求数据',
            'filePath': '文件路径(用于文件上传)',
        }
        api_case_type_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='api_case_type'
        )
        api_case_type_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in
                                api_case_type_list]
        api_case_type_option_dict = {item.get('value'): item for item in api_case_type_option}
        api_body_type_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='api_body_type'
        )
        api_body_type_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in
                                api_body_type_list]
        api_body_type_option_dict = {item.get('value'): item for item in api_body_type_option}
        for item in test_cases_list:
            if str(item.get('caseType')) in api_case_type_option_dict.keys():
                item['caseType'] = api_case_type_option_dict.get(str(item.get('caseType'))).get('label')
            if str(item.get('method')) in api_body_type_option_dict.keys():
                item['method'] = api_body_type_option_dict.get(str(item.get('method'))).get('label')
            if str(item.get('requestType')) in api_body_type_option_dict.keys():
                item['requestType'] = api_body_type_option_dict.get(str(item.get('requestType'))).get('label')
        binary_data = ExcelUtil.export_list2excel(test_cases_list, mapping_dict)

        return binary_data
