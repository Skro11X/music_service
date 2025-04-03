from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    MEMBER = "Member"


class YandexUserORM(Base):
    __tablename__ = "yandex_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[Role]
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str | None]
    file_path: Mapped[str | None]
    access_token: Mapped[str | None]

    files: Mapped[list["FileOrm"]] = relationship(back_populates="yandex_user")
