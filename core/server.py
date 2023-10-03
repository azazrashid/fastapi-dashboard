from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from core.config import config
from core.database.create_db import validate_database
from core.utils.utils import run_alembic_upgrade


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_db():
    validate_database()


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="FastAPI E-Commerce",
        description="FastAPI E-Commerce Dashboard",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=make_middleware(),
    )
    init_db()
    run_alembic_upgrade()
    init_routers(app_=app_)
    return app_


app = create_app()
