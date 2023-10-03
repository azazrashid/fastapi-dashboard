from pydantic import BaseModel

from app.models.models import Category


class CategoryResponse(BaseModel):
    id: int
    name: str


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: CategoryResponse

    class Config:
        orm_mode = True
