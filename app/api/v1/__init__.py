from fastapi import APIRouter

from .inventory import inventory_router
from .products import products_router
from .sales import sales_router
from .home import home_router
from .revenue import revenue_router


v1_router = APIRouter()
v1_router.include_router(home_router)
v1_router.include_router(inventory_router, prefix="/inventory")
v1_router.include_router(products_router, prefix="/products")
v1_router.include_router(sales_router, prefix="/sales")
v1_router.include_router(revenue_router, prefix="/revenue")
