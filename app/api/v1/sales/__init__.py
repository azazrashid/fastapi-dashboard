from fastapi import APIRouter, Depends
from .sales import router


sales_router = APIRouter()
sales_router.include_router(
    router,
    tags=["Sales"],
)

__all__ = ["sales_router"]
