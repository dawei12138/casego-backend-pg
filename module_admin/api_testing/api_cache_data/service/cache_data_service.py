import time

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from config.get_redis import RedisUtil
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_cache_data.dao.cache_data_dao import Cache_dataDao
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import DeleteCache_dataModel, Cache_dataModel, \
    Cache_dataPageQueryModel
from utils.excel_util import ExcelUtil
from utils.log_util import logger

from utils.page_util import get_page_obj


class Cache_dataService:
    """
    环境缓存模块服务层
    """

    @classmethod
    async def get_cachedata_by_key(cls, redis, query_object: Cache_dataPageQueryModel):
        """
        根据查询条件获取缓存变值：按照环境，userid分组
        :param redis:
        :param query_object:
            user_id = query_object.user_id
            cache_key = query_object.cache_key
            environment_id = query_object.environment_id
        :return: list
        """
        start_time = time.time()
        user_id = query_object.user_id
        cache_key = query_object.cache_key
        environment_id = query_object.environment_id

        if cache_key and environment_id is not None:
            query_key = f"environment_cache:user:{user_id}:env:{environment_id}:{cache_key}"
            logger.info(f"获取缓存；{query_key}")
            value = await redis.get(query_key)
            # logger.info(f"获取缓存；{time.time()-start_time}s")
            return value
        else:
            return None

    @classmethod
    async def query_redis_with_prefix(cls, redis, query_object: Cache_dataPageQueryModel):
        """
        根据查询条件获取缓存变量列表：按照环境，userid分组
        :param redis:
        :param query_object: 
        :return: list
        """

        user_id = query_object.user_id
        cache_key = query_object.cache_key
        environment_id = query_object.environment_id

        if cache_key and environment_id:
            query_key = f"environment_cache:user:{user_id}:env:{environment_id}:{cache_key}"
            value = await redis.get(query_key)
            res = [{"id": query_key, "cacheKey": cache_key,
                    "cacheValue": value}] if value else []
            return res
        elif cache_key and not environment_id:
            query_pattern = f"environment_cache:user:{user_id}:env:*:{cache_key}"
        elif environment_id and not cache_key:
            query_pattern = f"environment_cache:user:{user_id}:env:{environment_id}*"
        else:
            query_pattern = f"environment_cache:user:{user_id}:env*"

        # 使用 scan 非阻塞遍历
        cursor = b"0"
        matched_keys = []
        while cursor:
            cursor, partial_keys = await redis.scan(cursor=cursor, match=query_pattern, count=100)
            matched_keys.extend(partial_keys)

        if matched_keys:
            values = await redis.mget(*matched_keys)
            return [
                {"id": k, "cacheKey": k.split(":")[-1],
                 "cacheValue": (v if v else None)}
                for k, v in zip(matched_keys, values)
            ]
        else:
            return []

    @classmethod
    async def cache_data_detail_services(cls, redis, cache_id: Any):
        """
        获取环境缓存详细信息service

        :param redis:
        :param cache_id: 缓存数据ID
        :return: 缓存数据ID对应的信息
        """

        value = await redis.get(cache_id)
        res = {"id": cache_id, "cacheKey": cache_id.split(":")[-1],
               "cacheValue": value if value else None}
        return res

    @classmethod
    async def delete_by_keys(cls, redis, keys: List[str]) -> int:
        """
        根据完整 Redis key 列表批量删除
        :param redis:
        :param keys: Redis 完整键名列表
        :return: 实际删除的 key 数量
        """
        if not keys:
            return 0
        deleted = await redis.delete(*keys)
        return deleted

    @classmethod
    async def delete_by_key(cls, redis, key: str) -> bool:
        """
        删除单个key
        :param redis: Redis 连接
        :param key: Redis 键名
        :return: 是否成功删除（1表示成功，0表示key不存在）
        """
        deleted = await redis.delete(key)
        return deleted == 1

    @classmethod
    async def get_redis_cache_list_services(cls, redis, query_object: Cache_dataPageQueryModel,
                                            is_page: bool = False):
        """

        :param redis:
        :param is_page:
        :param query_object:
        :return: 获取redis的缓存变量
        """

        res = await Cache_dataService.query_redis_with_prefix(redis, query_object)
        if is_page:
            resault = get_page_obj(res, query_object.page_num, query_object.page_size)
            return resault
        else:
            return res

    @classmethod
    async def get_cache_data_list_services(
            cls, query_db: AsyncSession, query_object: Cache_dataPageQueryModel, is_page: bool = False
    ):
        """
        获取环境缓存列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境缓存列表信息对象
        """
        cache_data_list_result = await Cache_dataDao.get_cache_data_list(query_db, query_object, is_page)

        return cache_data_list_result

    @classmethod
    async def add_cache_data_services(cls, redis, edit_cache_data: Cache_dataModel):
        """
        通过完整 Redis key 新增或更新数据
        :param redis:
        :param edit_cache_data:
        :return: 成功返回 True
        """
        start_time = time.time()
        cache_key = f"environment_cache:user:{edit_cache_data.user_id}:env:{edit_cache_data.environment_id}:{edit_cache_data.cache_key}"
        try:
            if await redis.get(cache_key):
                await redis.set(cache_key, edit_cache_data.cache_value)
                # logger.info(f"设置缓存；{time.time()-start_time}s")
                return CrudResponseModel(is_success=True, message='新增成功')
            else:
                await redis.set(cache_key, edit_cache_data.cache_value)
                # logger.info(f"设置缓存；{time.time()-start_time}s")
                return CrudResponseModel(is_success=True, message='更新已有变量成功')
        except Exception as e:
            raise e

    @classmethod
    async def delete_cache_services(cls, redis, delete_cache_data: Cache_dataModel):
        """
        通过完整 Redis key 新增或更新数据
        :param delete_cache_data:
        :param redis:
        :param edit_cache_data:
        :return: 成功返回 True
        """
        start_time = time.time()
        cache_key = f"environment_cache:user:{delete_cache_data.user_id}:env:{delete_cache_data.environment_id}:{delete_cache_data.cache_key}"
        try:
            if await redis.get(cache_key):
                deleted = await redis.delete(cache_key)
                return deleted == 1

            else:
                return False
        except Exception as e:
            raise e

    @classmethod
    async def edit_cache_data_services(cls, redis, edit_cache_data: Cache_dataModel):
        """
        通过完整 Redis key 新增或更新数据
        :param redis:
        :param edit_cache_data:
        :return: 成功返回 True
        """
        if not edit_cache_data.id:
            ServiceException(message='环境缓存不存在')
        try:
            await redis.set(edit_cache_data.id, edit_cache_data.cache_value)
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as e:
            raise e

    @classmethod
    async def delete_cache_data_services(cls, redis, page_object: DeleteCache_dataModel):
        """
        删除环境缓存信息service

        :param redis:
        :param page_object: 删除环境缓存对象
        :return: 删除环境缓存校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:

                deleted = await redis.delete(*id_list)
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                raise e
        else:
            raise ServiceException(message='传入缓存数据ID为空')

    # @classmethod
    # async def cache_data_detail_services(cls, query_db: AsyncSession, id: int):
    #     """
    #     获取环境缓存详细信息service
    #
    #     :param query_db: orm对象
    #     :param id: 缓存数据ID
    #     :return: 缓存数据ID对应的信息
    #     """
    #     cache_data = await Cache_dataDao.get_cache_data_detail_by_id(query_db, id=id)
    #     if cache_data:
    #         result = Cache_dataModel(**CamelCaseUtil.transform_result(cache_data))
    #     else:
    #         result = Cache_dataModel(**dict())
    #
    #     return result

    @staticmethod
    async def export_cache_data_list_services(cache_data_list: List):
        """
        导出环境缓存信息service

        :param cache_data_list: 环境缓存信息列表
        :return: 环境缓存信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '缓存数据ID',
            'cacheKey': '缓存键名',
            'environmentId': '关联的环境ID',
            'cacheValue': '缓存值',
            'sourceType': '数据来源可以为空',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
            'userId': '用戶id',
        }
        binary_data = ExcelUtil.export_list2excel(cache_data_list, mapping_dict)

        return binary_data


if __name__ == '__main__':
    import asyncio


    async def main():
        db = await RedisUtil.create_redis_pool()
        try:
            query1 = Cache_dataPageQueryModel(cache_key="bibabo", environment_id=1, user_id="1",
                                              cache_value="123123312")
            await Cache_dataService.add_cache_data_services(db, query1)

            query = Cache_dataPageQueryModel(cache_key="bibabo", environment_id=1, user_id="1")
            value = await Cache_dataService.get_cachedata_by_key(db, query)
            print(value)
            pass
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            await db.close()


    asyncio.run(main())
