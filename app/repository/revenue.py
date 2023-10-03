from sqlalchemy import func, and_

from app.models.models import Sale, Product, Category
from app.schemas.responses.revenue import (
    RevenueCategory,
    RevenueProduct,
    RevenueDaily,
    RevenueWeekly,
    RevenueMonthly,
    RevenueAnnual,
    RevenueTimePeriod,
)
from core.utils.utils import get_month_abbr


async def calculate_daily_revenue(db, start_date, end_date):
    """
    Calculate daily revenue.

    Args:
        db: Database session.
        start_date: Start date of the date range.
        end_date: End date of the date range.

    Returns:
        List[RevenueDaily]: List of daily revenue data.
    """
    revenues = (
        db.query(Sale.date, func.sum(Sale.revenue).label("total_revenue"))
        .filter(Sale.date >= start_date, Sale.date <= end_date)
        .group_by(Sale.date)
        .all()
    )
    revenue_daily = [RevenueDaily(date=revenue[0], total_revenue=revenue[1]) for revenue in revenues]

    return revenue_daily


async def calculate_revenue_timeperiod(db, start_date, end_date):
    """
    Calculate total revenue within a specified time period.

    Args:
        db: Database session.
        start_date: Start date of the time period.
        end_date: End date of the time period.

    Returns:
        RevenueTimePeriod: Total revenue within the time period.
    """
    total_revenue = (
        db.query(func.sum(Sale.revenue))
        .filter(and_(Sale.date >= start_date, Sale.date <= end_date))
        .scalar()
    )

    if total_revenue is None:
        total_revenue = 0.0

    revenue_analysis = RevenueTimePeriod(
        time_period=f"{start_date} - {end_date}", total_revenue=total_revenue
    )

    return revenue_analysis


async def calculate_weekly_revenue(db, start_date, end_date):
    """
    Calculate weekly revenue.

    Args:
        db: Database session.
        start_date: Start date of the date range.
        end_date: End date of the date range.

    Returns:
        List[RevenueWeekly]: List of weekly revenue data.
    """
    revenues = (
        db.query(
            func.year(Sale.date).label("year"),
            func.week(Sale.date).label("week"),
            func.sum(Sale.revenue).label("total_revenue"),
        )
        .filter(Sale.date >= start_date, Sale.date <= end_date)
        .group_by("year", "week")
        .all()
    )

    revenue_weekly = [
        RevenueWeekly(week=f"Week {revenue[1]} - {revenue[0]}", total_revenue=revenue[2]) for revenue in revenues
    ]

    return revenue_weekly


async def calculate_monthly_revenue(db, start_date, end_date):
    """
    Calculate monthly revenue.

    Args:
        db: Database session.
        start_date: Start date of the date range.
        end_date: End date of the date range.

    Returns:
        List[RevenueMonthly]: List of monthly revenue data.
    """
    revenue = (
        db.query(
            func.year(Sale.date).label("year"),
            func.month(Sale.date).label("month"),
            func.sum(Sale.revenue).label("total_revenue"),
        )
        .filter(Sale.date >= start_date, Sale.date <= end_date)
        .group_by("year", "month")
        .all()
    )

    revenue_monthly = [
        RevenueMonthly(month=f"{get_month_abbr(revenue[1])} {revenue[0]}", total_revenue=revenue[2])
        for revenue in revenue
    ]

    return revenue_monthly


async def calculate_annual_revenue(db, start_date, end_date):
    """
    Calculate annual revenue.

    Args:
        db: Database session.
        start_date: Start date of the date range.
        end_date: End date of the date range.

    Returns:
        List[RevenueAnnual]: List of annual revenue data.
    """
    revenues = (
        db.query(
            func.year(Sale.date).label("year"),
            func.sum(Sale.revenue).label("total_revenue"),
        )
        .filter(Sale.date >= start_date, Sale.date <= end_date)
        .group_by("year")
        .all()
    )

    revenue_annual = [RevenueAnnual(year=revenue[0], total_revenue=revenue[1]) for revenue in revenues]

    return revenue_annual


async def calculate_products_revenue(db, product_ids):
    """
    Calculate revenue for a list of products.

    Args:
        db: Database session.
        product_ids: List of product IDs.

    Returns:
        List[RevenueProduct]: List of product revenue data.
    """
    revenues = (
        db.query(
            Product.name.label("name"), func.sum(Sale.revenue).label("total_revenue")
        )
        .join(Sale, Product.id == Sale.product_id)
        .filter(Product.id.in_(product_ids))
        .group_by(Product.name)
        .all()
    )
    revenue_product = [RevenueProduct(product=revenue[0], total_revenue=revenue[1]) for revenue in revenues]
    return revenue_product


async def calculate_category_revenue(db, category_ids):
    """
    Calculate revenue for a list of categories.

    Args:
        db: Database session.
        category_ids: List of category IDs.

    Returns:
        List[RevenueCategory]: List of category revenue data.
    """
    revenues = (
        db.query(
            Category.name.label("name"), func.sum(Sale.revenue).label("total_revenue")
        )
        .join(Product, Product.category_id == Category.id)
        .join(Sale, Product.id == Sale.product_id)
        .filter(Category.id.in_(category_ids))
        .group_by(Category.name)
        .all()
    )

    revenue_categories = [
        RevenueCategory(category=revenue[0], total_revenue=revenue[1]) for revenue in revenues
    ]

    return revenue_categories
