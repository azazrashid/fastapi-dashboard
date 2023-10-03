from fastapi import APIRouter

from .home import router

home_router = APIRouter()
home_router.include_router(router, tags=["Home"])

__all__ = ["home_router"]
