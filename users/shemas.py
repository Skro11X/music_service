from pydantic import BaseModel


class DeleteResponseShem(BaseModel):
    response: bool


class YandexUserSchem(BaseModel):

    username: str
    name: str | None

    class Config:
        from_attributes = True
