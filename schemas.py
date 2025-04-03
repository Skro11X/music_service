from pydantic import BaseModel


class YandexUserSchem(BaseModel):

    username: str
    name: str | None

    class Config:
        from_attributes = True


class FileShem(BaseModel):
    file_path: str
    file_name: str

    class Config:
        from_attributes = True


class FileWriteShem(FileShem):
    is_overwrite: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenDataShem(BaseModel):
    username: str | None = None


class DeleteResponseShem(BaseModel):
    response: bool
