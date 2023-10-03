from datetime import datetime
from random import randint, uniform, choice
from faker import Faker
from sqlalchemy.orm import Session
from app.models.models import Product, Category, Sale, Inventory
from core.database.session import get_connection
from core.database.create_db import validate_database
from core.utils.utils import run_alembic_upgrade

fake = Faker()


def create_demo_data(session: Session,
                     num_categories: int,
                     num_products: int,
                     num_sales: int):
    categories = []
    for _ in range(num_categories):
        category = Category(name=fake.word())
        session.add(category)
        session.commit()
        categories.append(category)

    products = []
    for _ in range(num_products):
        category = choice(categories)
        product = Product(
            name=fake.word(),
            description=fake.sentence(),
            price=uniform(10, 200),
            category_id=category.id,
        )
        session.add(product)
        session.commit()
        products.append(product)

    for _ in range(num_sales):
        product = choice(products)
        sale = Sale(
            date=fake.date_between(start_date='-2y', end_date='today'),
            quantity=randint(1, 10),
            revenue=uniform(10, 200),
            product_id=product.id,
        )
        session.add(sale)
        session.commit()

    for product in products:
        inventory = Inventory(
            product_id=product.id,
            quantity=randint(1, 50),
            date=datetime.now(),
        )
        session.add(inventory)

    session.commit()


if __name__ == "__main__":
    num_categories = 5
    num_products = 20
    num_sales = 100

    validate_database()  # create db it does not exist
    run_alembic_upgrade()  # create the tables
    with Session(get_connection()) as db:
        create_demo_data(db, num_categories, num_products, num_sales)
        print("Demo data populated successfully.")
