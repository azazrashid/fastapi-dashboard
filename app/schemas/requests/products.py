from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

    class Config:
        orm_mode = True
