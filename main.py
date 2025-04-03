<<<<<<< HEAD
from fastapi import FastAPI
from database import database_instance
from files.endpoints import router as files_router
from users.tokens_utils.endpoints import router as token_router
from users.endpoints import router as users_router
=======

from fastapi import FastAPI
from database import database_instance
from endpoints import router
>>>>>>> efe26fe3e9e4ea146b7e26103cb35b4f1c2185b3


def create_app():
    database_instance.create_database()
    app_instance = FastAPI()
<<<<<<< HEAD
    app_instance.include_router(files_router)
    app_instance.include_router(token_router)
    app_instance.include_router(users_router)
=======
    app_instance.include_router(router)
>>>>>>> efe26fe3e9e4ea146b7e26103cb35b4f1c2185b3
    return app_instance


app = create_app()
