from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.db.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Used ONLY by admins to update a user's role
class UserRoleUpdate(BaseModel):
    role: UserRole

# Used when returning user data to the client. The password is intentionally omitted.
class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

