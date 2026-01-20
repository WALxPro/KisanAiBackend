from fastapi import APIRouter, HTTPException
from models import ItemCreate, ItemUpdate, ItemResponse
import crud

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Create a new item."""
    return await crud.create_item(item)


@router.get("/", response_model=list[ItemResponse])
async def get_items(skip: int = 0, limit: int = 100):
    """Get all items."""
    return await crud.get_all_items(skip, limit)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Get a single item by ID."""
    item = await crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemUpdate):
    """Update an item by ID."""
    updated = await crud.update_item(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    """Delete an item by ID."""
    deleted = await crud.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
