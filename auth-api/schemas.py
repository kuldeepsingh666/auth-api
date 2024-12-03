from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: EmailStr


class UserCreate(UserSchema):
    password: constr(min_length=8, max_length=120)


class UserUpdate(UserSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    designation: Optional[str]
    department: Optional[str]


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
