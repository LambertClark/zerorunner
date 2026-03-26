# -*- coding: utf-8 -*-
"""
PC 图片文件管理服务
- 支持 UploadFile 上传
- 支持 base64 图片保存
- 返回可访问的下载 URL
- 使用 config.UPLOAD_DIR 和 config.FILE_BASE_URL
"""
import base64
import os
import uuid
import typing
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from loguru import logger

from config import config

# 允许上传的图片扩展名
_ALLOWED_EXTS = {"png", "jpg", "jpeg", "bmp", "gif", "webp"}


def _check_image_ext(ext: str):
    if ext.lower() not in _ALLOWED_EXTS:
        raise ValueError(f"不支持的图片格式: .{ext}，允许格式: {_ALLOWED_EXTS}")


def _get_upload_dir() -> str:
    upload_dir = getattr(config, "UPLOAD_DIR", None) or config.TEST_FILES_DIR
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


def _build_url(filename: str) -> str:
    """拼接可访问的图片 URL"""
    base_url = getattr(config, "FILE_BASE_URL", config.BASE_URL).rstrip("/")
    return f"{base_url}/pc/fm/download/{filename}"


class PcFileManagerService:
    """PC图片文件管理服务"""

    @staticmethod
    async def upload_image(file: UploadFile) -> typing.Dict[str, str]:
        """上传图片文件"""
        if not file:
            raise FileNotFoundError("请选择上传文件")
        ext_parts = (file.filename or "").split(".")
        ext = ext_parts[-1] if len(ext_parts) > 1 else ""
        _check_image_ext(ext)

        file_name = f"{uuid.uuid4().hex.upper()}.{ext}"
        upload_dir = _get_upload_dir()
        abs_path = Path(upload_dir).joinpath(file_name).as_posix()

        contents = await file.read()
        async with aiofiles.open(abs_path, "wb") as f:
            await f.write(contents)

        logger.info(f"PC图片上传: {abs_path}")
        return {
            "filename": file_name,
            "url": _build_url(file_name),
            "original_name": file.filename,
            "size": len(contents),
        }

    @staticmethod
    async def save_base64_image(
        base64_content: str,
        filename: str = "image.png",
    ) -> typing.Dict[str, str]:
        """保存 base64 编码图片"""
        if not base64_content:
            raise ValueError("base64内容不能为空")

        # 去掉 data URI 前缀（如 data:image/png;base64,）
        if "," in base64_content:
            base64_content = base64_content.split(",", 1)[1]

        ext_parts = filename.split(".")
        ext = ext_parts[-1] if len(ext_parts) > 1 else "png"
        _check_image_ext(ext)

        file_name = f"{uuid.uuid4().hex.upper()}.{ext}"
        upload_dir = _get_upload_dir()
        abs_path = Path(upload_dir).joinpath(file_name).as_posix()

        contents = base64.b64decode(base64_content)
        async with aiofiles.open(abs_path, "wb") as f:
            await f.write(contents)

        logger.info(f"PC图片(base64)保存: {abs_path}")
        return {
            "filename": file_name,
            "url": _build_url(file_name),
            "original_name": filename,
            "size": len(contents),
        }

    @staticmethod
    def get_abs_path(filename: str) -> str:
        """根据文件名返回绝对路径（用于下载接口）"""
        upload_dir = _get_upload_dir()
        return Path(upload_dir).joinpath(filename).as_posix()
