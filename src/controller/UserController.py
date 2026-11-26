from fastapi import HTTPException, status

from src.schema.AuthSchema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from src.service.AuthService import AuthService


class UserController:
    @staticmethod
    async def register_user(user_data: RegisterRequest) -> RegisterResponse:

        try:
            user = await AuthService.register_user(user_data)

            return RegisterResponse(
                id=str(user.id), email=user.email, message="Registration successful"
            )

        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @staticmethod
    async def login_user(user_data: LoginRequest) -> LoginResponse:

        try:
            return await AuthService.login_user(user_data)

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
