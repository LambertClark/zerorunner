# -*- coding: utf-8 -*-
import os
import typing

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from autotest.services.pc_autotest.pc_file_manager_service import PcFileManagerService
from autotest.utils.response.http_response import partner_success

router = APIRouter()


class Base64ImageIn(BaseModel):
    base64_content: str
    filename: str = "image.png"


@router.post("/uploadImage", description="上传PC图片素材")
async def upload_image(file: UploadFile = File(...)):
    data = await PcFileManagerService.upload_image(file)
    return partner_success(data)


@router.post("/uploadBase64", description="保存base64图片素材")
async def upload_base64(params: Base64ImageIn):
    data = await PcFileManagerService.save_base64_image(params.base64_content, params.filename)
    return partner_success(data)


@router.get("/download/{filename}", description="下载PC图片素材")
async def download_image(filename: str):
    abs_path = PcFileManagerService.get_abs_path(filename)
    if not os.path.isfile(abs_path):
        return HTMLResponse(content="文件不存在", status_code=404)
    return FileResponse(path=abs_path, filename=filename)
