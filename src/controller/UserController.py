from src.schema.AuthSchema import RegisterIncoming, RegisterResponse
from src.service.AuthService import AuthService

from fastapi import HTTPException, status


class UserController:
    async def register_user_controller(
        self, user_request: RegisterIncoming
    ) -> RegisterResponse:

        try:
            response = await AuthService.register(user_request)

            return RegisterResponse(
                id=str(response.id),
                email=response.email,
                message="User registered successfully",
            )

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )
