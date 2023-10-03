from sqlalchemy import Column, Integer, String, ForeignKey, Index, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    # Establishes a bidirectional relationship with requests (one-to-many)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    # Defines a foreign key to represent the requests's category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Establish a bidirectional relationship with Category
    category = relationship("Category", back_populates="products")
    # Establishes a bidirectional relationship with sales (one-to-many)
    inventory = relationship("Inventory", back_populates="product")
    sales = relationship("Sale", back_populates="products")

    # Adds an index for name for optimized searching
    __table_args__ = (Index("idx_product_name", "name"),)


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Defines a foreign key to represent the requests in inventory
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Establishes a bidirectional relationship with requests (many-to-one)
    product = relationship("Product", back_populates="inventory")

    # Adds an index for date for optimized filtering
    __table_args__ = (Index("idx_inventory_date", "date"),)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    products = relationship("Product", back_populates="sales")

    # indexes for date and product_id for optimized filtering
    __table_args__ = (
        Index("idx_sale_date", "date"),
        Index("idx_sale_product_id", "product_id"),
    )
