import os
from datetime import timedelta
from typing import Annotated

import aiofiles
import requests
from fastapi import UploadFile, APIRouter, Request, Header, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from database import database_instance
from models import YandexUserORM
from repository import UserRepository
from schemas import Token, YandexUserSchem
from tokens import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, get_current_user

router = APIRouter()

ClientID = '033faf2f43c74087ae0f06e2989e4ce7'
Secret = 'c6dc0ff0b714431f95832bf309f1542e'



@router.post("/file")
async def upload_file(file: UploadFile,
                      filename: str = None):
    if not file.content_type.startswith('audio/'):
        return {'wrong': 'wrong file type'}
    if filename is None:
        filename = file.filename
    file_path = os.path.join('./files', filename)
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    return {'good': 'file sent to server'}


@router.get("/register")
def register():
    return RedirectResponse('https://oauth.yandex.ru/authorize?response_type=code&client_id=033faf2f43c74087ae0f06e2989e4ce7')


@router.get("/yandex_login")
def login(code: str):
    response = requests.post('https://oauth.yandex.ru/token', data={'grant_type': 'authorization_code', 'code': code,
                                                                    'client_id': ClientID, 'client_secret': Secret})
    data = response.json()
    user_info = requests.post('https://login.yandex.ru/info', data={'oauth_token': data.get('access_token'),
                                                                    'format': 'json'}).json()
    UserRepository.get_or_create(username=user_info['login'])

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_info["login"]}, expires_delta=access_token_expires
    )
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/token")
async def login_for_access_token(
    current_user: Annotated[YandexUserSchem, Depends(get_current_user)],
) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=YandexUserSchem)
async def read_users_me(
    current_user: Annotated[YandexUserSchem, Depends(get_current_user)],
):
    return current_user
