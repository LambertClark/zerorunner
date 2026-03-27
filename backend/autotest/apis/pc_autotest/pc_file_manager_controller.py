# -*- coding: utf-8 -*-
import base64
import os
import uuid
from pathlib import Path
from typing import List

import aiofiles
from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse

from autotest.models.pc_picture_models import PcPictureInfo as PictureInfo
from autotest.services.pc_autotest.pc_file_manager_service import PcFileManagerService
from autotest.utils.response.http_response import partner_success
from config import config

UPLOAD_DIR = config.UPLOAD_DIR
BASE_URL = config.FILE_BASE_URL
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

pcFmService = PcFileManagerService()

router = APIRouter()


@router.post("/upload-photo", description="上传PC图片素材")
async def upload_photo(file: UploadFile = File(...)):
    result = await pcFmService.save_upload_file(file)
    name = result["filename"]
    image_url = result["path"]
    tree_id = None
    table_type = None
    table_id = None
    picture = await PictureInfo.create_or_update({
        "name": name,
        "url": image_url,
        "tree_id": tree_id,
        "table_type": table_type,
        "table_id": table_id,
    })
    picture_id = picture.get("id") if isinstance(picture, dict) else getattr(picture, "id", None)
    return partner_success({**result, "picture_id": picture_id})


@router.post("/upload-multiple", description="批量上传PC图片素材")
async def upload_multiple_photos(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            result = await pcFmService.save_upload_file(file)
            results.append({**result, "status": "success"})
        except HTTPException as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": e.detail,
            })
    return partner_success(results)


@router.post("/upload-base64", description="上传base64图片素材")
async def upload_base64_image(base64_image: str):
    try:
        if "," in base64_image:
            base64_image = base64_image.split(",", 1)[1]
        # 补齐 padding
        base64_image += "=" * (-len(base64_image) % 4)
        base64.b64decode(base64_image)
        return partner_success({"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"错误: {str(e)}"})


@router.get("/download/{filename}", description="下载PC图片素材")
async def download_file(filename: str):
    file_path = pcFmService.upload_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(str(file_path), filename=filename)
