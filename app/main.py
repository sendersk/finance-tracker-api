from fastapi import FastAPI

from app.api.routes import router
from app.core.config import APP_NAME
from app.core.logger import setup_logger

setup_logger()

app = FastAPI(title=APP_NAME)

app.include_router(router)