from bson import ObjectId
from database import get_db
from models import ItemCreate, ItemUpdate


# Collection name
COLLECTION = "items"


async def create_item(item: ItemCreate) -> dict:
    """Create a new item."""
    db = get_db()
    item_dict = item.model_dump()
    result = await db[COLLECTION].insert_one(item_dict)
    created = await db[COLLECTION].find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created


async def get_all_items(skip: int = 0, limit: int = 100) -> list:
    """Get all items with pagination."""
    db = get_db()
    items = []
    cursor = db[COLLECTION].find().skip(skip).limit(limit)
    async for item in cursor:
        item["_id"] = str(item["_id"])
        items.append(item)
    return items


async def get_item(item_id: str) -> dict | None:
    """Get a single item by ID."""
    db = get_db()
    if not ObjectId.is_valid(item_id):
        return None
    item = await db[COLLECTION].find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"])
    return item


async def update_item(item_id: str, item: ItemUpdate) -> dict | None:
    """Update an item by ID."""
    db = get_db()
    if not ObjectId.is_valid(item_id):
        return None

    # Only include fields that are not None
    update_data = {k: v for k, v in item.model_dump().items() if v is not None}

    if not update_data:
        return await get_item(item_id)

    await db[COLLECTION].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )
    return await get_item(item_id)


async def delete_item(item_id: str) -> bool:
    """Delete an item by ID."""
    db = get_db()
    if not ObjectId.is_valid(item_id):
        return False
    result = await db[COLLECTION].delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0
