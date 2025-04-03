from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body

from files.shemas import FileShem
from users.db_models import YandexUserORM
from users.repository import UserRepository
from users.shemas import YandexUserSchem, DeleteResponseShem
from users.tokens_utils.tokens import get_current_user, check_admin_user

router = APIRouter(prefix="/users")


@router.get("/me/", response_model=YandexUserSchem)
async def read_users_me(
    current_user: Annotated[YandexUserORM, Depends(get_current_user)],
):
    return YandexUserSchem.model_validate(current_user)


@router.post("/me/", response_model=YandexUserSchem)
def update_users_me(
    current_user: Annotated[YandexUserORM, Depends(get_current_user)],
    body: dict | None = Body(),
):
    if body is None:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="empty response",
        )
    UserRepository.update(current_user, body)
    return YandexUserSchem.model_validate(current_user)


@router.post("/delete", response_model=DeleteResponseShem)
def delete_users(
    current_user: Annotated[YandexUserORM, Depends(check_admin_user)],
    user_id: int = Body(embed=True, default=0),
):
    is_deleted = UserRepository.delete(user_id=user_id)
    return DeleteResponseShem(response=is_deleted)


@router.get("/me/files/", response_model=list[FileShem])
def list_of_files(
    current_user: Annotated[YandexUserORM, Depends(get_current_user)],
):
    return UserRepository.get_files_from_user(current_user)
