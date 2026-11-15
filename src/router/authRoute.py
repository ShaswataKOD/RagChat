from fastapi import APIRouter, status

from src.schema.AuthSchema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from src.controller.UserController import UserController


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: RegisterRequest):
    return await UserController.register_user(user_data)


@auth_router.post(
    "/login", response_model=LoginResponse, status_code=status.HTTP_200_OK
)
async def login_user(user_data: LoginRequest):
    return await UserController.login_user(user_data)
