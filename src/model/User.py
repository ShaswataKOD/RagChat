from datetime import datetime, timezone
from enum import Enum


from beanie import Document
from pydantic import EmailStr, Field, field_validator
from pymongo import ASCENDING, IndexModel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class User(Document):
    email: EmailStr
    hashed_password: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value

    class Settings:
        name = "users"
        indexes = [IndexModel([("email", ASCENDING)], unique=True)]
