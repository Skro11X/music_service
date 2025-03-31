from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import Insert
from database import database_instance
from models import YandexUserORM


class UserRepository:
    @classmethod
    def create_or_update(cls, dict_of_new_info: dict, **kwargs) -> YandexUserORM:
        with (database_instance.session() as session):
            query = Insert(YandexUserORM).values(**kwargs).on_conflict_do_update(
                index_elements=["username"],
                set_=dict_of_new_info
            ).returning(YandexUserORM.username)
            result = session.execute(query)
            session.commit()
            return result.fetchone()

    @classmethod
    def exists(cls, **kwargs) -> YandexUserORM | None:
        with database_instance.session() as session:
            query = select(YandexUserORM).filter_by(**kwargs)
            response = session.execute(query).scalars().first()
            return response

    @classmethod
    def change_token(cls, token, new_token):
        with database_instance.session() as session:
            query = update(YandexUserORM).values(access_token=new_token).filter_by(access_token=token)
            result = session.execute(query)
            session.commit()
            return result

    @classmethod
    def update(cls, user, for_update_args) -> YandexUserORM | None:
        with database_instance.session() as session:
            for key, value in for_update_args.items():
                if key == "username" or key == "access_token":
                    continue
                setattr(user, key, value)
            session.add(user)
            session.commit()
            return user
