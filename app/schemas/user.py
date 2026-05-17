from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: EmailStr
    full_name: str = Field(min_length=1, max_length=100)


class UserRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    email: EmailStr
    full_name: str
    created_at: datetime


class UserListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[UserRead]
    total: int = Field(ge=0)
