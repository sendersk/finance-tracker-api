from fastapi import FastAPI

from app.core.config import APP_NAME
from app.core.logger import setup_logger
from app.db.database import create_tables
from app.routes.health import router as health_router
from app.routes.transactions import router as transaction_router

setup_logger()

create_tables()

app = FastAPI(title=APP_NAME)

app.include_router(health_router)
app.include_router(transaction_router)