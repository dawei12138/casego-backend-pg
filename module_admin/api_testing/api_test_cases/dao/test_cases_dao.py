from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.api_testing.api_assertions.dao.assertions_dao import AssertionsDao
from module_admin.api_testing.api_assertions.entity.vo.assertions_vo import AssertionsPageQueryModel, \
    AssertionsQueryModel
from module_admin.api_testing.api_cookies.dao.cookies_dao import CookiesDao
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesPageQueryModel, CookiesQueryModel
from module_admin.api_testing.api_formdata.dao.formdata_dao import FormdataDao
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataPageQueryModel, FormdataQueryModel
from module_admin.api_testing.api_headers.dao.headers_dao import HeadersDao
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersPageQueryModel, HeadersQueryModel
from module_admin.api_testing.api_params.dao.params_dao import ParamsDao
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsPageQueryModel, ParamsQueryModel
from module_admin.api_testing.api_setup.dao.setup_dao import SetupDao
from module_admin.api_testing.api_setup.entity.vo.setup_vo import SetupPageQueryModel, SetupQueryModel
from module_admin.api_testing.api_teardown.dao.teardown_dao import TeardownDao
from module_admin.api_testing.api_teardown.entity.vo.teardown_vo import TeardownPageQueryModel, TeardownQueryModel
from module_admin.api_testing.api_test_cases.entity.do.test_cases_do import ApiTestCases
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesModel, Test_casesPageQueryModel, \
    Test_casesAllParamsQueryModel
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil
from config.get_db import get_db


class Test_casesDao:
    """
    接口用例模块数据库操作层
    """

    @classmethod
    async def get_test_cases_detail_by_id(cls, db: AsyncSession, case_id: int):
        """
        根据测试用例ID获取接口用例详细信息

        :param db: orm对象
        :param case_id: 测试用例ID
        :return: 接口用例信息对象
        """
        test_cases_info = (
            (
                await db.execute(
                    select(ApiTestCases)
                    .where(
                        ApiTestCases.case_id == case_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return test_cases_info

    @classmethod
    async def get_test_cases_all_detail_by_id(cls, db: AsyncSession, case_id: int) -> Test_casesAllParamsQueryModel:
        """
        根据测试用例ID获取接口用例详细信息

        :param db: orm对象
        :param case_id: 测试用例ID
        :return: 接口用例信息对象
        """

        test_case = await Test_casesDao.get_test_cases_detail_by_id(db, case_id=case_id)
        if test_case:
            test_case_result = Test_casesAllParamsQueryModel(**CamelCaseUtil.transform_result(test_case))
            test_case_result.cookies_list = await CookiesDao.get_cookies_orm_list(db,
                                                                                  CookiesQueryModel(case_id=case_id))
            test_case_result.headers_list = await HeadersDao.get_headers_orm_list(db,
                                                                                  HeadersQueryModel(case_id=case_id))
            test_case_result.params_list = await ParamsDao.get_params_orm_list(db, ParamsQueryModel(case_id=case_id))
            test_case_result.assertion_list = await AssertionsDao.get_assertions_orm_list(db, AssertionsQueryModel(
                case_id=case_id))
            test_case_result.setup_list = await SetupDao.get_setup_orm_list(db, SetupQueryModel(case_id=case_id))
            test_case_result.teardown_list = await TeardownDao.get_teardown_orm_list(db, TeardownQueryModel(
                case_id=case_id))
            test_case_result.formdata = await FormdataDao.get_formdata_orm_list(db, FormdataQueryModel(case_id=case_id))
            return test_case_result
        else:
            return None

    @classmethod
    async def get_test_cases_detail_by_info(cls, db: AsyncSession, test_cases: Test_casesModel):
        """
        根据接口用例参数获取接口用例信息

        :param db: orm对象
        :param test_cases: 接口用例参数对象
        :return: 接口用例信息对象
        """
        test_cases_info = (
            (
                await db.execute(
                    select(ApiTestCases).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return test_cases_info

    @classmethod
    async def get_test_cases_list(cls, db: AsyncSession, query_object: Test_casesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口用例列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口用例列表信息对象
        """
        query = (
            select(ApiTestCases)
            .where(
                ApiTestCases.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiTestCases.case_type == query_object.case_type if query_object.case_type else True,
                ApiTestCases.copy_id == query_object.copy_id if query_object.copy_id else True,
                ApiTestCases.parent_case_id == query_object.parent_case_id if query_object.parent_case_id else True,
                ApiTestCases.parent_submodule_id == query_object.parent_submodule_id if query_object.parent_submodule_id else True,
                ApiTestCases.description == query_object.description if query_object.description else True,
                ApiTestCases.path == query_object.path if query_object.path else True,
                ApiTestCases.method == query_object.method if query_object.method else True,
                ApiTestCases.request_type == query_object.request_type if query_object.request_type else True,
                ApiTestCases.is_run == query_object.is_run if query_object.is_run else True,
                ApiTestCases.status_code == query_object.status_code if query_object.status_code else True,
                ApiTestCases.sleep == query_object.sleep if query_object.sleep else True,
                ApiTestCases.sort_no == query_object.sort_no if query_object.sort_no else True,
                ApiTestCases.file_path == query_object.file_path if query_object.file_path else True,
            )
            .where(ApiTestCases.del_flag == "0")
            .order_by(ApiTestCases.case_id)
            #.distinct()
        )
        test_cases_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return test_cases_list

    @classmethod
    async def get_test_cases_orm_list(cls, db: AsyncSession, query_object: Test_casesPageQueryModel):
        """
        根据查询参数获取接口用例列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口用例列表信息orm对象
        """
        query = (
            select(ApiTestCases)
            .where(
                ApiTestCases.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiTestCases.case_type == query_object.case_type if query_object.case_type else True,
                ApiTestCases.copy_id == query_object.copy_id if query_object.copy_id else True,
                ApiTestCases.parent_case_id == query_object.parent_case_id if query_object.parent_case_id else True,
                ApiTestCases.parent_submodule_id == query_object.parent_submodule_id if query_object.parent_submodule_id else True,
                ApiTestCases.description == query_object.description if query_object.description else True,
                ApiTestCases.path == query_object.path if query_object.path else True,
                ApiTestCases.method == query_object.method if query_object.method else True,
                ApiTestCases.request_type == query_object.request_type if query_object.request_type else True,
                ApiTestCases.is_run == query_object.is_run if query_object.is_run else True,
                ApiTestCases.status_code == query_object.status_code if query_object.status_code else True,
                ApiTestCases.sleep == query_object.sleep if query_object.sleep else True,
                ApiTestCases.sort_no == query_object.sort_no if query_object.sort_no else True,
                ApiTestCases.data == query_object.data if query_object.data else True,
                ApiTestCases.file_path == query_object.file_path if query_object.file_path else True,
            )
            .where(ApiTestCases.del_flag == "0")
            .order_by(ApiTestCases.case_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_test_cases_dao(cls, db: AsyncSession, test_cases: Test_casesModel):
        """
        新增接口用例数据库操作

        :param db: orm对象
        :param test_cases: 接口用例对象
        :return:
        """
        db_test_cases = ApiTestCases(**test_cases.model_dump(exclude={'del_flag', }))
        db.add(db_test_cases)
        await db.flush()

        return db_test_cases

    @classmethod
    async def edit_test_cases_dao(cls, db: AsyncSession, test_cases: dict):
        """
        编辑接口用例数据库操作

        :param db: orm对象
        :param test_cases: 需要更新的接口用例字典
        :return:
        """

        await db.execute(update(ApiTestCases), [test_cases])

    @classmethod
    async def delete_test_cases_dao(cls, db: AsyncSession, test_cases: Test_casesModel):
        """
        删除接口用例数据库操作

        :param db: orm对象
        :param test_cases: 接口用例对象
        :return:
        """
        # await db.execute(delete(ApiTestCases).where(ApiTestCases.case_id.in_([test_cases.case_id])))
        await db.execute(update(ApiTestCases).where(ApiTestCases.case_id.in_([test_cases.case_id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Test_casesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Test_casesDao.get_test_cases_all_detail_by_id(db, 1)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
