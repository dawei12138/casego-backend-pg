from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from config.get_db import get_db
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesModel, \
    Test_casesAllParamsQueryModel
from module_admin.api_testing.api_test_cases.service.test_cases_service import Test_casesService
from utils.log_util import logger

# 导入MCP实例
from module_fastmcp.mcp_instance import mcp

#
# class BatchRequest(BaseModel):
#     """批量处理请求"""
#     items: List[str] = Field(..., description="待处理项目")
#     operation: str = Field(..., description="操作类型: upper/lower")
#
#
# class BatchResponse(BaseModel):
#     """批量处理响应"""
#     processed_items: List[str]
#     count: int
#
