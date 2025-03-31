from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class YandexUserORM(Base):
    __tablename__ = 'yandex_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str | None]
    access_token: Mapped[str | None]

    # files: Mapped[list["FileOrm"]] = relationship()


class FileOrm(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(unique=True)
    file_path: Mapped[str] = mapped_column(unique=True)
    # user: Mapped[int] = mapped_column(ForeignKey(column="yandex_user.id", ondelete="CASCADE"))
    #
    # yandex_user: Mapped["YandexUserORM"] = relationship()
