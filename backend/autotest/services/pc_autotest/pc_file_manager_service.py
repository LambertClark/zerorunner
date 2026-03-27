# -*- coding: utf-8 -*-
import base64
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile, HTTPException

from config import config

_ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
_MAX_SIZE = 5 * 1024 * 1024

_MIME_TO_EXT = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/webp': 'webp',
}


def validate_image(file: UploadFile):
    """验证图片类型（仅允许 image/jpeg, image/png, image/webp）"""
    if file.content_type not in _ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f'不支持的图片类型: {file.content_type}，仅允许: {sorted(_ALLOWED_MIME_TYPES)}',
        )


def generate_unique_filename(original_name: str) -> str:
    """生成唯一文件名"""
    parts = original_name.rsplit('.', 1)
    ext = parts[-1] if len(parts) > 1 else 'png'
    return f'{uuid.uuid4().hex.upper()}.{ext}'


def _parse_image_suffix(header: str) -> str:
    """从 base64 header 解析后缀，e.g. data:image/png;base64 → png"""
    try:
        mime = header.split(';')[0].split(':')[1].strip()
        return _MIME_TO_EXT.get(mime, 'png')
    except (IndexError, AttributeError):
        return 'png'


class PcFileManagerService:
    """PC图片文件管理服务"""

    def __init__(
        self,
        upload_dir: str = config.UPLOAD_DIR,
        base_url: str = config.FILE_BASE_URL,
    ):
        self.upload_dir = Path(upload_dir)
        self.base_url = base_url.rstrip('/')
        self._init_upload_dir()

    def _init_upload_dir(self):
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload_file(self, file: UploadFile) -> dict:
        validate_image(file)
        filename = generate_unique_filename(file.filename or 'image.png')
        save_path = self.upload_dir / filename
        content_buf = b''
        async with aiofiles.open(save_path, 'wb') as f:
            while True:
                chunk = await file.read(64 * 1024)
                if not chunk:
                    break
                await f.write(chunk)
                content_buf += chunk
        if len(content_buf) > _MAX_SIZE:
            save_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=f'文件大小超过限制 {_MAX_SIZE} bytes')
        return self._build_response_data(filename, save_path)

    async def save_base64_image(self, base64_data: str) -> dict:
        try:
            if ',' in base64_data:
                header, encoded = base64_data.split(',', 1)
                ext = _parse_image_suffix(header)
            else:
                encoded = base64_data
                ext = 'png'
            image_bytes = base64.b64decode(encoded)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Base64 解码失败: {str(e)}')
        filename = f'{uuid.uuid4().hex.upper()}.{ext}'
        save_path = self.upload_dir / filename
        async with aiofiles.open(save_path, 'wb') as f:
            await f.write(image_bytes)
        return self._build_response_data(filename, save_path)

    def _build_response_data(self, filename: str, save_path: Path) -> dict:
        return {
            'filename': filename,
            'path': f'{self.base_url}/api/pc/fm/download/{filename}',
            'size': save_path.stat().st_size,
        }
