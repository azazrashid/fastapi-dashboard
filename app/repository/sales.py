from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from app.models.models import Sale, Product, Category
from app.schemas.responses.sales import (
    ProductSales,
    CategorySales,
    ProductTimePeriod,
    SalesAnalysis,
)


async def get_sales_db(db: Session, offset: int, limit: int):
    """
    Retrieve sales data with pagination.

    Args:
        db: Database session.
        offset: Offset for pagination.
        limit: Maximum number of records to retrieve.

    Returns:
        List[Sale]: List of sales records.
    """
    sales = (
        db.query(Sale)
        .offset(offset)
        .limit(limit)
        .options(joinedload(Sale.products))
        .all()
    )
    return sales


async def get_sales_date(db: Session, start_date: date, end_date: date):
    """
    Get total sales within a date range.

    Args:
        db: Database session.
        start_date: Start date of the date range.
        end_date: End date of the date range.

    Returns:
        ProductTimePeriod: Total sales within the date range.
    """
    query = (
        select(
            func.sum(Sale.quantity).label("total_sales"),
        )
        .filter(Sale.date >= start_date)
        .filter(Sale.date <= end_date)
    )
    sales = db.exec(query).first()

    sales = ProductTimePeriod(date=f"{start_date} - {end_date}", total_sales=sales)
    return sales


async def get_sales_product(db: Session, product_id):
    """
    Get total sales for a specific product.

    Args:
        db: Database session.
        product_id: ID of the product to retrieve sales for.

    Returns:
        Union[ProductSales, None]: Product sales data or None if the product is not found.
    """
    query = (
        select(
            Product.id.label("product_id"),
            func.sum(Sale.quantity).label("total_sales"),
            Product.name.label("product_name"),
        )
        .join(Product, Product.id == Sale.product_id)
        .filter(Sale.product_id == product_id)
        .group_by(Product.id,Product.name)
    )

    products = db.exec(query).first()

    if products:
        return ProductSales(
            product_id=products.product_id,
            product_name=products.product_name,
            total_sales=products.total_sales
        )
    else:
        return None


async def get_sales_category(db: Session, category_id):
    """
    Get total sales for a specific category.

    Args:
        db: Database session.
        category_id: ID of the category to retrieve sales for.

    Returns:
        Union[CategorySales, None]: Category sales data or None if the category
         is not found.
    """
    query = (
        select(
            Category.id.label("category_id"),
            func.sum(Sale.quantity).label("total_sales"),
            Category.name.label("category_name"),
        )
        .join(Product, Product.id == Sale.product_id)
        .join(Category, Category.id == Product.category_id)
        .filter(Category.id == category_id)
        .group_by(Category.id,Category.name)
    )

    categories = db.exec(query).first()

    if categories:
        return CategorySales(
            category_id= categories.category_id,
            category_name=categories.category_name,
            total_sales=categories.total_sales
        )
    else:
        return None


async def sales_analysis(db: Session) -> SalesAnalysis:
    """
    Analyze sales data.

    Args:
        db: Database session.

    Returns:
        SalesAnalysis: Analysis results including total sales, average revenue,
        sales per product, and sales per category.
    """
    # Calculate total sales (number of sale quantities)
    total_sales = db.query(func.sum(Sale.quantity)).scalar()

    # Calculate average revenue per sale
    average_revenue = db.query(func.avg(Sale.revenue)).scalar()

    # Calculate sales per product
    sales_per_product = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            func.sum(Sale.quantity).label("total_sales"),
        )
        .join(Sale, Product.id == Sale.product_id)
        .group_by(Product.id,Product.name)
        .all()
    )

    # Calculate sales per category
    sales_per_category = (
        db.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.sum(Sale.quantity).label("total_sales"),
        )
        .join(Product, Product.category_id == Category.id)
        .join(Sale, Product.id == Sale.product_id)
        .group_by(Category.id,Category.name)
        .all()
    )

    analysis = SalesAnalysis(
        total_sales=total_sales,
        average_revenue=average_revenue,
        sales_per_product=sales_per_product,
        sales_per_category=sales_per_category,
    )

    return analysis
