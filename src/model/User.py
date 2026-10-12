from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from beanie import Document


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class User(Document):
    name: Optional[str] = None
    email: EmailStr
    hashedPassword: str
    gender: Optional[Gender]

    class Settings:
        name = "users"
