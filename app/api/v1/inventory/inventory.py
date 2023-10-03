from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.repository.inventory import get_inventory, update_inventory_db
from app.schemas.requests.inventory import InventoryUpdate
from app.schemas.responses.inventory import InventoryChange, InventoryStatus
from core.database.session import get_session

router = APIRouter()


@router.get("/", response_model=List[InventoryStatus])
async def get_inventory_status(
    low_stock_threshold: int = 10,
    db: Session = Depends(get_session),
):
    inventory_status = await get_inventory(
        db=db, low_stock_threshold=low_stock_threshold
    )

    return inventory_status


@router.post("/update", response_model=InventoryChange)
async def update_inventory(
    update_data: InventoryUpdate, db: Session = Depends(get_session)
):
    inventory_change = await update_inventory_db(db=db, update_data=update_data)

    return inventory_change
