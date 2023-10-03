from datetime import date

from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session

from app.repository.sales import (
    get_sales_db,
    get_sales_date,
    get_sales_product,
    get_sales_category,
    sales_analysis,
)
from app.schemas.responses.sales import SalesAnalysis
from core.database.session import get_session

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_sales(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_session),
):
    sales = await get_sales_db(db=db, offset=offset, limit=limit)
    return sales


@router.get("/date")
async def filter_sales_date(
    start_date: date = Query(),
    end_date: date = Query(),
    db: Session = Depends(get_session),
):
    sales = await get_sales_date(
        db=db,
        start_date=start_date,
        end_date=end_date,
    )
    return sales


@router.get("/product")
async def filter_sales_product(
    product_id: int = Query(),
    db: Session = Depends(get_session),
):
    sales = await get_sales_product(
        db=db,
        product_id=product_id,
    )
    return sales


@router.get("/category")
async def filter_sales_category(
    category_id: int = Query(),
    db: Session = Depends(get_session),
):
    category = await get_sales_category(
        db=db,
        category_id=category_id,
    )
    return category


@router.get("/analyze", response_model=SalesAnalysis)
async def analyze_sales(db: Session = Depends(get_session)):
    analysis = await sales_analysis(db=db)
    return analysis
