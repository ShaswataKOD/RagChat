from src.model.User import User
from src.schema.AuthSchema import RegisterRequest
from src.util.encode_password import hash_password
from src.schema.AuthSchema import LoginRequest, LoginResponse
from src.util.verify_password import verify_password
from src.util.generate_token import create_access_token


class AuthService:
    @staticmethod
    async def register_user(user_data: RegisterRequest):

        email = user_data.email

        # Check if user already exists
        existing_user = await User.find_one(User.email == email)

        if existing_user:
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create user
        new_user = User(email=email, hashed_password=hashed_password)

        await new_user.insert()

        return new_user

    @staticmethod
    async def login_user(user_data: LoginRequest):

        email = user_data.email

        # Find user
        user = await User.find_one(User.email == email)

        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        is_valid = verify_password(user_data.password, user.hashed_password)

        if not is_valid:
            raise ValueError("Invalid email or password")

        # Generate JWT
        access_token = create_access_token(str(user.id))

        return LoginResponse(access_token=access_token, token_type="bearer")
