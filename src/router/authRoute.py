from controller.UserController import UserAuthentication
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

auth_router.post("/register")(UserAuthentication.registerUser)
