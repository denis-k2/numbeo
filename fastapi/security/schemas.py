from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class Roles(Enum):
    user = "user"
    admin = "admin"


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Roles = "user"
    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    hashed_password: str
    active: bool = False
    role: Roles
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
