from pydantic import BaseModel


class InventoryStatus(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    low_stock: bool


class InventoryChange(BaseModel):
    product_id: int
    product_name: str
    quantity_change: int
    new_quantity: int
