from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(str):
    """Custom type for MongoDB ObjectId."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


# ============ Item Models ============

class ItemCreate(BaseModel):
    """Schema for creating a new item."""
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class ItemUpdate(BaseModel):
    """Schema for updating an item (all fields optional)."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None


class ItemResponse(BaseModel):
    """Schema for item response."""
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

    class Config:
        populate_by_name = True
