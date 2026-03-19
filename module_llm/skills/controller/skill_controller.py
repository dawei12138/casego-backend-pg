from datetime import datetime

from fastapi import APIRouter, Depends, Form, Query, Request, UploadFile, File
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_llm.skills.service.skill_service import SkillService
from module_llm.skills.entity.vo.skill_vo import (
    DeleteSkillModel, SkillModel, SkillPageQueryModel,
    SkillFileModel, SkillImportUrlModel,
)
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

skillController = APIRouter(prefix='/skills/skill', dependencies=[Depends(LoginService.get_current_user)])


# ==================== 技能 CRUD ====================


@skillController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:list'))],
    summary='获取技能列表',
    description='根据查询条件获取技能分页列表数据',
)
async def get_skill_list(
    request: Request,
    skill_page_query: SkillPageQueryModel = Depends(SkillPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    skill_page_query_result = await SkillService.get_skill_list_services(
        query_db, skill_page_query, is_page=True
    )
    return ResponseUtil.success(model_content=skill_page_query_result)


@skillController.get(
    '/all',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:list'))],
    summary='获取所有技能',
    description='获取所有技能列表（用于下拉选择）',
)
async def get_skill_all(
    request: Request,
    skill_page_query: SkillPageQueryModel = Depends(SkillPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    skill_all_result = await SkillService.get_skill_all_list_services(query_db, skill_page_query)
    return ResponseUtil.success(data=skill_all_result)


@skillController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='新增技能',
    description='手动创建一个新的技能',
)
@ValidateFields(validate_model='add_skill')
async def add_skill(
    request: Request,
    add_skill: SkillModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_skill.create_by = current_user.user.user_name
    add_skill.create_time = datetime.now()
    add_skill.update_by = current_user.user.user_name
    add_skill.update_time = datetime.now()
    add_skill_result = await SkillService.add_skill_services(query_db, add_skill)
    return ResponseUtil.success(msg=add_skill_result.message)


@skillController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='修改技能',
    description='根据主键更新技能信息',
)
@ValidateFields(validate_model='edit_skill')
async def edit_skill(
    request: Request,
    edit_skill: SkillModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_skill.update_by = current_user.user.user_name
    edit_skill.update_time = datetime.now()
    edit_skill_result = await SkillService.edit_skill_services(query_db, edit_skill)
    return ResponseUtil.success(msg=edit_skill_result.message)


@skillController.delete(
    '/{skill_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:remove'))],
    summary='删除技能',
    description='根据主键批量删除技能，多个主键以逗号分隔',
)
async def delete_skill(request: Request, skill_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_skill_obj = DeleteSkillModel(skillIds=skill_ids)
    delete_skill_result = await SkillService.delete_skill_services(query_db, delete_skill_obj)
    return ResponseUtil.success(msg=delete_skill_result.message)


@skillController.get(
    '/{skill_id}',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:query'))],
    summary='获取技能详情',
    description='根据主键获取技能详细信息（含文件列表）',
)
async def query_detail_skill(request: Request, skill_id: str, query_db: AsyncSession = Depends(get_db)):
    skill_detail_result = await SkillService.skill_detail_services(query_db, skill_id)
    return ResponseUtil.success(data=skill_detail_result)


# ==================== 导入/导出 ====================


@skillController.post(
    '/upload',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='上传技能包',
    description='上传ZIP文件导入技能',
)
async def upload_skill(
    request: Request,
    file: UploadFile = File(...),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        zip_bytes = await file.read()
        result = await SkillService.upload_skill_services(
            query_db, zip_bytes, current_user.user.user_name
        )
        return ResponseUtil.success(msg=result.message)
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'上传失败: {str(e)}')


@skillController.post(
    '/import-url',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='URL导入技能',
    description='从URL地址导入技能（支持SKILL.md原始链接或ZIP文件链接）',
)
async def import_url_skill(
    request: Request,
    import_model: SkillImportUrlModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        result = await SkillService.import_url_skill_services(
            query_db, import_model, current_user.user.user_name
        )
        return ResponseUtil.success(msg=result.message)
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'导入失败: {str(e)}')


@skillController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:export'))],
    summary='导出技能列表',
    description='导出技能列表数据到Excel文件',
)
async def export_skill_list(
    request: Request,
    skill_page_query: SkillPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    skill_query_result = await SkillService.get_skill_list_services(
        query_db, skill_page_query, is_page=False
    )
    skill_export_result = await SkillService.export_skill_list_services(skill_query_result)
    return ResponseUtil.streaming(data=bytes2file_response(skill_export_result))


# ==================== 文件操作 ====================


@skillController.get(
    '/{skill_id}/files',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:query'))],
    summary='获取技能文件列表',
    description='获取技能目录中的所有文件列表（不含内容）',
)
async def get_skill_files(
    request: Request,
    skill_id: str,
    query_db: AsyncSession = Depends(get_db),
):
    files_result = await SkillService.get_skill_files_services(query_db, skill_id)
    return ResponseUtil.success(data=files_result)


@skillController.get(
    '/{skill_id}/file',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:query'))],
    summary='获取技能文件内容',
    description='根据技能ID和文件相对路径获取文件内容',
)
async def get_skill_file_content(
    request: Request,
    skill_id: str,
    file_path: str = Query(..., description='文件相对路径'),
    query_db: AsyncSession = Depends(get_db),
):
    file_result = await SkillService.get_skill_file_content_services(query_db, skill_id, file_path)
    return ResponseUtil.success(data=file_result)


@skillController.post(
    '/{skill_id}/file',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='新增技能文件',
    description='向技能目录中添加新文件',
)
async def add_skill_file(
    request: Request,
    skill_id: str,
    file_model: SkillFileModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    file_model.skill_id = skill_id
    file_model.create_by = current_user.user.user_name
    file_model.create_time = datetime.now()
    file_model.update_by = current_user.user.user_name
    file_model.update_time = datetime.now()
    result = await SkillService.add_skill_file_services(query_db, file_model)
    return ResponseUtil.success(msg=result.message)


@skillController.put(
    '/{skill_id}/file',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='编辑技能文件',
    description='更新技能目录中的文件内容',
)
async def edit_skill_file(
    request: Request,
    skill_id: str,
    file_model: SkillFileModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    file_model.skill_id = skill_id
    file_model.update_by = current_user.user.user_name
    file_model.update_time = datetime.now()
    result = await SkillService.edit_skill_file_services(query_db, file_model)
    return ResponseUtil.success(msg=result.message)


@skillController.delete(
    '/{skill_id}/file/{file_id}',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:remove'))],
    summary='删除技能文件',
    description='从技能目录中删除指定文件',
)
async def delete_skill_file(
    request: Request,
    skill_id: str,
    file_id: str,
    query_db: AsyncSession = Depends(get_db),
):
    result = await SkillService.delete_skill_file_services(query_db, skill_id, file_id)
    return ResponseUtil.success(msg=result.message)
