from fastapi import APIRouter, Depends
from .inventory import router


inventory_router = APIRouter()
inventory_router.include_router(
    router,
    tags=["Inventory"],
)

__all__ = ["inventory_router"]
