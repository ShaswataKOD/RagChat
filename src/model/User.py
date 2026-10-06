from enum import Enum

from pydantic import BaseModel, EmailStr
from beanie import Document


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class User(Document):
    name: str
    email: EmailStr
    hashedPassword: str
    gender: Gender
