from sqlalchemy import insert, select
from sqlalchemy.dialects.postgresql import Insert
from database import database_instance
from models import YandexUserORM
from schemas import YandexUserSchem

class UserRepository:
    @classmethod
    def get_or_create(cls, **kwargs) -> YandexUserORM:
        with (database_instance.session() as session):
            query = Insert(YandexUserORM).values(**kwargs).on_conflict_do_nothing().returning(YandexUserORM.username)
            result = session.execute(query)
            session.commit()
            return result.fetchone()

    @classmethod
    def get_all(cls) -> YandexUserORM:
        with database_instance.session() as session:
            query = select(YandexUserORM)
            result = session.execure(query)
            user_model = result.all()
            return user_model

    @classmethod
    def exists(cls, **kwargs) -> YandexUserSchem | None:
        with database_instance.session() as session:
            query = select(YandexUserORM).filter_by(**kwargs)
            response = session.execute(query).scalars().first()
            user = YandexUserSchem.model_validate(response)
            return user