
from fastapi import FastAPI
from database import database_instance
from endpoints import router


def create_app():
    database_instance.create_database()
    app_instance = FastAPI()
    app_instance.include_router(router)
    return app_instance


app = create_app()
