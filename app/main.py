from fastapi import FastAPI

from app.api.routes import router
from app.core.config import APP_NAME
from app.core.logger import setup_logger
from app.db.database import create_tables

setup_logger()

create_tables()

app = FastAPI(title=APP_NAME)

app.include_router(router)