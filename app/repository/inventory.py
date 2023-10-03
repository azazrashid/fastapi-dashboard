from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.models import Product, Inventory
from app.schemas.requests.inventory import InventoryUpdate
from app.schemas.responses.inventory import InventoryStatus, InventoryChange


async def get_inventory(db: Session, low_stock_threshold: int) -> list[InventoryStatus]:
    """
    Retrieve inventory status, including low stock alerts.

    Args:
        db (Session): The database session.
        low_stock_threshold (int): The threshold for low stock alerts.

    Returns:
        list[InventoryStatus]: A list of inventory statuses.
    """
    inventory = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Inventory.quantity.label("current_quantity"),
        )
        .join(Inventory, Product.id == Inventory.product_id)
        .all()
    )

    inventory_status = []

    for each in inventory:
        low_stock_alert = each.current_quantity <= low_stock_threshold
        inventory_status.append(
            InventoryStatus(
                product_id=each.product_id,
                product_name=each.product_name,
                current_quantity=each.current_quantity,
                low_stock=low_stock_alert,
            )
        )

    return inventory_status


async def update_inventory_db(db: Session, update_data: InventoryUpdate):
    """
    Update inventory levels and track changes over time.

    Args:
        db (Session): The database session.
        update_data (InventoryUpdate): The data to update inventory.

    Raises:
        HTTPException: If the product is not found.

    Returns:
        InventoryChange: Information about the inventory change.
    """
    product = db.query(Product).filter(Product.id == update_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == update_data.product_id)
        .first()
    )

    change_in_quantity = update_data.quantity_change

    if inventory:
        inventory.quantity += change_in_quantity
    else:
        inventory = Inventory(
            product_id=update_data.product_id, quantity=change_in_quantity
        )
        db.add(inventory)

    db.commit()

    inventory_change = InventoryChange(
        product_id=product.id,
        product_name=product.name,
        quantity_change=change_in_quantity,
        new_quantity=inventory.quantity,
    )

    return inventory_change
