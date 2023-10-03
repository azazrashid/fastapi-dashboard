from fastapi import status, HTTPException
from app.models.models import Product, Category
from sqlmodel import Session, select
from app.schemas.requests.products import ProductCreate
from sqlalchemy.orm import joinedload


async def get_products_db(db: Session, offset: int, limit: int) -> list[Product]:
    """
    Retrieve a list of products from the database.

    Args:
        db (Session): The database session.
        offset (int): The starting index of products to retrieve.
        limit (int): The maximum number of products to retrieve.

    Returns:
        list[Product]: A list of product objects.
    """
    query = (
        select(Product)
        .offset(offset)
        .limit(limit)
        .options(joinedload(Product.category))
    )
    products = db.exec(query).all()
    return products


async def create_product(db: Session, product: ProductCreate) -> dict:
    """
    Create a new product and add it to the database.

    Args:
        db (Session): The database session.
        product (ProductCreate): The product data to create.

    Raises:
        HTTPException: If the specified category does not exist.

    Returns:
        dict: Information about the created product.
    """
    category = (
        db.query(Category).where(Category.id == product.category_id).one_or_none()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Create a response dictionary
    response_data = {
        "id": db_product.id,
        "name": db_product.name,
        "description": db_product.description,
        "price": db_product.price,
        "category": {
            "id": category.id,
            "name": category.product,
        },
    }

    return response_data
