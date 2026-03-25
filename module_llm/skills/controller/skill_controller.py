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
    SkillFileContentSaveModel, SkillFilesBatchSaveModel,
    SkillFolderCreateModel, SkillFolderRenameModel,
    SkillFolderDeleteModel, SkillFileMoveModel,
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
    summary='获取技能列表(分页)',
    description='分页查询技能列表，支持按名称、状态等条件过滤',
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
    summary='获取全部技能列表',
    description='获取所有技能的简要信息列表，不分页',
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
    description='新增一个技能记录，自动创建SKILL.md文件',
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
    description='修改技能信息，支持重命名和状态变更',
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
    description='根据技能ID批量删除技能及其关联文件，同步移除文件系统',
)
async def delete_skill(request: Request, skill_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_skill_obj = DeleteSkillModel(skillIds=skill_ids)
    delete_skill_result = await SkillService.delete_skill_services(query_db, delete_skill_obj)
    return ResponseUtil.success(msg=delete_skill_result.message)


@skillController.post(
    '/sync-all',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='Sync all enabled skills',
    description='Sync all enabled skills from database to file system',
)
async def sync_all_skills(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
):
    result = await SkillService.sync_all_skills_services(query_db)
    return ResponseUtil.success(msg='sync all skills success', data=result)


@skillController.get(
    '/{skill_id}',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:query'))],
    summary='获取技能详情',
    description='根据技能ID查询技能详细信息，包含文件列表',
)
async def query_detail_skill(request: Request, skill_id: str, query_db: AsyncSession = Depends(get_db)):
    skill_detail_result = await SkillService.skill_detail_services(query_db, skill_id)
    return ResponseUtil.success(data=skill_detail_result)


# ==================== 导入/导出 ====================


@skillController.post(
    '/upload',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='上传导入技能',
    description='上传ZIP或MD文件导入技能，自动解析并创建记录',
)
async def upload_skill(
    request: Request,
    file: UploadFile = File(...),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        file_bytes = await file.read()
        result = await SkillService.upload_skill_services(
            query_db, file_bytes, file.filename, current_user.user.user_name
        )
        return ResponseUtil.success(msg=result.message)
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'导入失败: {str(e)}')


@skillController.post(
    '/import-url',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='URL导入技能',
    description='从URL导入技能，支持SKILL.md直链或ZIP压缩包地址',
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
    description='将技能列表导出为Excel文件下载',
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


# ==================== 文件管理 ====================


@skillController.get(
    '/{skill_id}/files',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:query'))],
    summary='获取技能文件列表',
    description='获取技能下所有文件的元信息列表，不含文件内容',
)
async def get_skill_files(
    request: Request,
    skill_id: str,
    query_db: AsyncSession = Depends(get_db),
):
    files_result = await SkillService.get_skill_files_services(query_db, skill_id)
    return ResponseUtil.success(data=files_result)


@skillController.put(
    '/{skill_id}/file/content',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='Save single skill file content',
    description='Upsert a single file by filePath and optionally trigger full sync',
)
async def save_skill_file_content(
    request: Request,
    skill_id: str,
    file_model: SkillFileContentSaveModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    result = await SkillService.save_skill_file_content_services(
        query_db,
        skill_id,
        file_model,
        current_user.user.user_name,
    )
    return ResponseUtil.success(msg='save skill file content success', data=result)


@skillController.put(
    '/{skill_id}/files/content',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='Save batch skill files content',
    description='Batch upsert files by filePath and optionally trigger full sync',
)
async def save_skill_files_batch(
    request: Request,
    skill_id: str,
    batch_model: SkillFilesBatchSaveModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    result = await SkillService.save_skill_files_batch_services(
        query_db,
        skill_id,
        batch_model,
        current_user.user.user_name,
    )
    return ResponseUtil.success(msg='save skill files batch success', data=result)


@skillController.get(
    '/{skill_id}/file',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:query'))],
    summary='获取技能文件内容',
    description='根据技能ID和文件路径获取文件内容',
)
async def get_skill_file_content(
    request: Request,
    skill_id: str,
    file_path: str | None = Query(None, alias='filePath', description='Skill relative file path'),
    file_path_legacy: str | None = Query(None, alias='file_path', include_in_schema=False),
    query_db: AsyncSession = Depends(get_db),
):
    target_file_path = file_path or file_path_legacy
    if not target_file_path:
        return ResponseUtil.failure(msg='filePath cannot be empty')

    file_result = await SkillService.get_skill_file_content_services(query_db, skill_id, target_file_path)
    return ResponseUtil.success(data=file_result)


@skillController.post(
    '/{skill_id}/file',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:add'))],
    summary='新增技能文件',
    description='为指定技能新增一个文件',
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
    summary='修改技能文件',
    description='修改技能下指定文件的信息或内容',
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
    description='删除技能下指定的文件',
)
async def delete_skill_file(
    request: Request,
    skill_id: str,
    file_id: str,
    query_db: AsyncSession = Depends(get_db),
):
    result = await SkillService.delete_skill_file_services(query_db, skill_id, file_id)
    return ResponseUtil.success(msg=result.message)


# ==================== 文件夹管理 ====================


@skillController.post(
    '/{skill_id}/folder',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='新增技能子文件夹',
    description='在技能目录下新增子文件夹，自动创建.gitkeep占位文件，自动同步到文件系统',
)
async def create_skill_folder(
    request: Request,
    skill_id: str,
    folder_model: SkillFolderCreateModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    result = await SkillService.create_skill_folder_services(
        query_db, skill_id, folder_model, current_user.user.user_name
    )
    return ResponseUtil.success(msg='创建文件夹成功', data=result)


@skillController.put(
    '/{skill_id}/folder/rename',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='重命名技能子文件夹',
    description='重命名技能下的子文件夹，自动更新所有子文件路径，自动同步到文件系统',
)
async def rename_skill_folder(
    request: Request,
    skill_id: str,
    folder_model: SkillFolderRenameModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    result = await SkillService.rename_skill_folder_services(
        query_db, skill_id, folder_model, current_user.user.user_name
    )
    return ResponseUtil.success(msg='重命名文件夹成功', data=result)


@skillController.delete(
    '/{skill_id}/folder',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:remove'))],
    summary='删除技能子文件夹',
    description='删除技能下的子文件夹及其所有文件，自动同步到文件系统',
)
async def delete_skill_folder(
    request: Request,
    skill_id: str,
    folder_model: SkillFolderDeleteModel,
    query_db: AsyncSession = Depends(get_db),
):
    result = await SkillService.delete_skill_folder_services(query_db, skill_id, folder_model)
    return ResponseUtil.success(msg='删除文件夹成功', data=result)


@skillController.put(
    '/{skill_id}/file/move',
    dependencies=[Depends(CheckUserInterfaceAuth('skills:skill:edit'))],
    summary='移动技能文件',
    description='将技能文件移动到新路径，自动同步到文件系统',
)
async def move_skill_file(
    request: Request,
    skill_id: str,
    move_model: SkillFileMoveModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    result = await SkillService.move_skill_file_services(
        query_db, skill_id, move_model, current_user.user.user_name
    )
    return ResponseUtil.success(msg='移动文件成功', data=result)
