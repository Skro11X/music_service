from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class FileOrm(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(unique=True)
    file_path: Mapped[str]
    user: Mapped[int] = mapped_column(
        ForeignKey(column="yandex_user.id", ondelete="CASCADE")
    )

    yandex_user: Mapped["YandexUserORM"] = relationship(
        back_populates="files", overlaps="files"
    )
