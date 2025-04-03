import os
import requests
from datetime import timedelta
from typing import Annotated
from fastapi import status, Depends, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from users.db_models import Role, YandexUserORM
from users.repository import UserRepository
from users.tokens_utils.tokens import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from users.tokens_utils.shemas import Token


ClientID = os.getenv("ClientID")
Secret = os.getenv("Secret")

router = APIRouter(prefix="/auth")


@router.get("/yandex/")
def register(code: str = ""):
    if code == "":
        return RedirectResponse(
            f"https://oauth.yandex.ru/authorize?response_type=code&client_id={ClientID}"
        )
    response = requests.post(
        "https://oauth.yandex.ru/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": ClientID,
            "client_secret": Secret,
        },
    )
    if response.status_code != 200:
        return JSONResponse(response.json(), status_code=status.HTTP_400_BAD_REQUEST)
    data = response.json()
    user_info = requests.post(
        "https://login.yandex.ru/info",
        data={"oauth_token": data.get("access_token"), "format": "json"},
    )
    if user_info.status_code != 200:
        return JSONResponse(user_info.json(), status_code=status.HTTP_400_BAD_REQUEST)
    user_info = user_info.json()
    # todo выводить ошибку в случае запросов с ошибкой.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_info["login"]}, expires_delta=access_token_expires
    )
    user = UserRepository.create_or_update(
        access_token=access_token, username=user_info["login"], role=Role.MEMBER
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/refresh")
async def login_for_access_token(
    current_user: Annotated[YandexUserORM, Depends(get_current_user)],
) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    UserRepository.change_token(current_user.access_token, access_token)
    return Token(access_token=access_token, token_type="bearer")
