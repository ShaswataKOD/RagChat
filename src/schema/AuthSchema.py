#  register incoming and returning for type safety
from pydantic import BaseModel, EmailStr


class RegisterIncoming(BaseModel):
    email: EmailStr
    password: str
    name = None
    gender = None


class RegisterResponse(BaseModel):
    email: EmailStr
    id: str
    message: str
