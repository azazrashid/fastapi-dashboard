from typing import List
from pydantic import BaseModel
from datetime import date


class ProductTimePeriod(BaseModel):
    date: str
    total_sales: int


class ProductSales(BaseModel):
    product_id: int
    product_name: str
    total_sales: int


class CategorySales(BaseModel):
    category_id: int
    category_name: str
    total_sales: int


class SalesAnalysis(BaseModel):
    total_sales: int
    average_revenue: float
    sales_per_product: List[ProductSales]
    sales_per_category: List[CategorySales]


class Sales(BaseModel):
    id: int
    date: date
    quantity: int
    revenue: float
    product_id: int

    class Config:
        orm_mode = True
