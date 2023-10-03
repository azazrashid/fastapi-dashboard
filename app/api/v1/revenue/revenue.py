from datetime import date, timedelta
from typing import List

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.repository.revenue import (
    calculate_daily_revenue,
    calculate_revenue_timeperiod,
    calculate_weekly_revenue,
    calculate_monthly_revenue,
    calculate_annual_revenue,
    calculate_products_revenue,
    calculate_category_revenue,
)
from app.schemas.responses.revenue import (
    RevenueCategory,
    RevenueProduct,
    RevenueDaily,
    RevenueWeekly,
    RevenueMonthly,
    RevenueAnnual,
    RevenueTimePeriod,
)
from core.database.session import get_session

router = APIRouter()


@router.get("/timeperiod", response_model=RevenueTimePeriod)
async def revenue_across_periods(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_session),
):
    revenue_analysis = await calculate_revenue_timeperiod(
        db=db, start_date=start_date, end_date=end_date
    )
    return revenue_analysis


@router.get("/daily", response_model=List[RevenueDaily])
async def daily_revenue(
    days: int = 7, db: Session = Depends(get_session)
):
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    revenue_daily = await calculate_daily_revenue(
        db=db, start_date=start_date, end_date=end_date
    )

    return revenue_daily


@router.get("/weekly", response_model=List[RevenueWeekly])
async def weekly_revenue(
    weeks: int = 4, db: Session = Depends(get_session)
):
    end_date = date.today()
    start_date = end_date - timedelta(weeks=weeks)

    revenue_weekly = await calculate_weekly_revenue(
        db=db, start_date=start_date, end_date=end_date
    )

    return revenue_weekly


@router.get("/monthly", response_model=List[RevenueMonthly])
async def monthly_revenue(
    months: int = 6, db: Session = Depends(get_session)
):
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)

    revenue_monthly = await calculate_monthly_revenue(
        db=db, start_date=start_date, end_date=end_date
    )

    return revenue_monthly


@router.get("/annual", response_model=List[RevenueAnnual])
async def annual_revenue(
    years: int = 3, db: Session = Depends(get_session)
):
    end_date = date.today()
    start_date = end_date - relativedelta(years=years)

    revenue_annual = await calculate_annual_revenue(
        db=db, start_date=start_date, end_date=end_date
    )

    return revenue_annual


@router.get("/products", response_model=List[RevenueProduct])
async def revenue_across_products(
    product_ids: List[int] = Query(..., description="List of product IDs to compare"),
    db: Session = Depends(get_session),
):
    revenue_product = await calculate_products_revenue(db, product_ids)

    return revenue_product


@router.get("/categories", response_model=List[RevenueCategory])
async def revenue_across_categories(
    category_ids: List[int] = Query(..., description="List of category IDs to compare"),
    db: Session = Depends(get_session),
):
    revenue_categories = await calculate_category_revenue(
        db=db, category_ids=category_ids
    )

    return revenue_categories
