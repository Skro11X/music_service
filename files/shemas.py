from pydantic import BaseModel


class FileShem(BaseModel):
    file_path: str
    file_name: str

    class Config:
        from_attributes = True


class FileWriteShem(FileShem):
    is_overwrite: bool
