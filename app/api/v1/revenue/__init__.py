from fastapi import APIRouter, Depends
from .revenue import router


revenue_router = APIRouter()
revenue_router.include_router(
    router,
    tags=["Revenue"],
)

__all__ = ["revenue_router"]
