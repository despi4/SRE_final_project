from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not _EMAIL_RE.fullmatch(normalized):
            raise ValueError("Invalid email format.")
        return normalized


class UserRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    email: str = Field(min_length=3, max_length=254)
    full_name: str
    created_at: datetime


class UserListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[UserRead]
    total: int = Field(ge=0)
