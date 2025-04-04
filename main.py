from fastapi import FastAPI
from database import database_instance
from files.endpoints import router as files_router
from users.tokens_utils.endpoints import router as token_router
from users.endpoints import router as users_router


def create_app():
    database_instance.create_database()
    app_instance = FastAPI()
    app_instance.include_router(files_router)
    app_instance.include_router(token_router)
    app_instance.include_router(users_router)
    return app_instance


app = create_app()
