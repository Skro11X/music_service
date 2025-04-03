from sqlalchemy.dialects.postgresql import Insert
from database import database_instance
from files.db_models import FileOrm

class FileRepository:
    @classmethod
    def create_new_file(cls, **kwargs):
        with database_instance.session() as session:
            query = Insert(FileOrm).values(**kwargs).on_conflict_do_nothing()
            result = session.execute(query).scalar()
            session.commit()
            return result
