from fastapi import APIRouter, Depends
from .products import product_router


products_router = APIRouter()
products_router.include_router(
    product_router,
    tags=["Products"],
)

__all__ = ["products_router"]
