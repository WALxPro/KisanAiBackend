from bson import ObjectId
from database import get_db
from models.admin_model import AdminCreate, AdminResponse   # root se import

# Collection name
COLLECTION = "admins"


async def create_admin(admin: AdminCreate) -> dict:
    """Create a new admin user."""
    db = get_db()
    admin_dict = admin.model_dump()
    result = await db[COLLECTION].insert_one(admin_dict)
    created = await db[COLLECTION].find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created


async def get_all_admins(skip: int = 0, limit: int = 100) -> list:
    """Get all admins with pagination."""
    db = get_db()
    admins = []
    cursor = db[COLLECTION].find().skip(skip).limit(limit)
    async for admin in cursor:
        admin["_id"] = str(admin["_id"])
        admins.append(admin)
    return admins


async def get_admin(admin_id: str) -> dict | None:
    """Get a single admin by ID."""
    db = get_db()
    if not ObjectId.is_valid(admin_id):
        return None
    admin = await db[COLLECTION].find_one({"_id": ObjectId(admin_id)})
    if admin:
        admin["_id"] = str(admin["_id"])
    return admin


async def update_admin(admin_id: str, admin: AdminCreate) -> dict | None:
    """Update an admin by ID."""
    db = get_db()
    if not ObjectId.is_valid(admin_id):
        return None

    update_data = {k: v for k, v in admin.model_dump().items() if v is not None}

    if not update_data:
        return await get_admin(admin_id)

    await db[COLLECTION].update_one(
        {"_id": ObjectId(admin_id)},
        {"$set": update_data}
    )
    return await get_admin(admin_id)


async def delete_admin(admin_id: str) -> bool:
    """Delete an admin by ID."""
    db = get_db()
    if not ObjectId.is_valid(admin_id):
        return False
    result = await db[COLLECTION].delete_one({"_id": ObjectId(admin_id)})
    return result.deleted_count > 0
