import os
from random import choices
from string import ascii_letters
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import joinedload

from database import database_instance
from models import YandexUserORM


class UserRepository:
    @classmethod
    def create_or_update(cls, **kwargs) -> YandexUserORM:
        with (database_instance.session() as session):
            query = Insert(YandexUserORM).values(**kwargs).on_conflict_do_update(
                index_elements=["username"],
                set_={"access_token": kwargs.get("access_token")}
            ).returning(YandexUserORM)
            result = session.execute(query).scalar_one()
            if result.file_path is None:
                folder_path = "files/"+result.username
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                else:
                    os.makedirs(folder_path+''.join(choices(ascii_letters, k=12)))
                result.file_path = folder_path
            session.commit()
            return result

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

    @classmethod
    def delete(self, user_id):
        with database_instance.session() as session:
            query = delete(YandexUserORM).where(YandexUserORM.id==user_id)
            session.execute(query)
            session.commit()
            return True

    @classmethod
    def get_files_from_user(cls, user):
        with database_instance.session() as session:
            query = select(YandexUserORM).where(YandexUserORM.id==user.id)
            result = session.execute(query).scalars()
            return result.first().files

