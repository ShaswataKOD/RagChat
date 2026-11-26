from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128, pattern=r"^[a-zA-Z0-9]+$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    id: str
    email: EmailStr
    message: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
