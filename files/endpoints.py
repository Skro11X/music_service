import os
from typing import Annotated

import aiofiles
from fastapi import Depends, UploadFile, APIRouter
from files.repository import FileRepository
from files.shemas import FileWriteShem
from users.db_models import YandexUserORM
from users.tokens_utils.tokens import get_current_user

router = APIRouter(prefix="/file")


@router.post("/")
async def upload_file(
    current_user: Annotated[YandexUserORM, Depends(get_current_user)],
    file: UploadFile,
    filename: str = None,
):
    if not file.content_type.startswith("audio/"):
        return {"wrong": "wrong file type"}
    if filename is None:
        filename = file.filename
    file_path = os.path.join(current_user.file_path, filename)
    is_overwrite = False
    if os.path.exists(file_path):
        is_overwrite = True
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
        FileRepository.create_new_file(
            file_path=current_user.file_path, file_name=filename, user=current_user.id
        )
        return FileWriteShem(
            file_path=current_user.file_path,
            file_name=filename,
            is_overwrite=is_overwrite,
        )
