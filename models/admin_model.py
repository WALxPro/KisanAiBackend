from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class PyObjectId(str):
    """Custom type for MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        from bson import ObjectId
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# ---------- Admin Schemas ----------

class AdminCreate(BaseModel):
    email: EmailStr
    full_name: str
    photo_url: str
    provider: str
    role: str = "admin"  # default role
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email: EmailStr
    full_name: str
    photo_url: str
    provider: str
    role: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
