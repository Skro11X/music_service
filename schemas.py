from pydantic import BaseModel


class YandexUserSchem(BaseModel):

    username: str
    name: str | None

    class Config:
        from_attributes = True

class YandexUserNewNameSchem(BaseModel):

    name: str

class FileShem(BaseModel):

    id: int
    file_name: str
    file_path: str
    user: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None