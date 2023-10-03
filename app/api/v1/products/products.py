from sqlmodel import Session
from fastapi import APIRouter, Depends, status
from core.database.session import get_session
from app.schemas.requests.products import ProductCreate
from app.schemas.responses.products import ProductResponse

from app.repository.products import get_products_db, create_product


product_router = APIRouter()


@product_router.get("/", status_code=status.HTTP_200_OK)
async def get_products(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_session),
):
    products = await get_products_db(db=db, offset=offset, limit=limit)
    return products


@product_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
)
async def register_product(
    product: ProductCreate,
    db: Session = Depends(get_session),
):
    db_product = await create_product(db=db, product=product)
    return db_product
