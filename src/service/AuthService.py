from src.schema.AuthSchema import RegisterIncoming
from src.model.User import User

from argon2 import PasswordHasher

ph = PasswordHasher()


class AuthService:
    @staticmethod
    async def register(user_data: RegisterIncoming) -> User:

        email = user_data.email
        password = user_data.password

        # Check if user already exists
        user = await User.find_one(User.email == email)

        if user:
            raise ValueError("User already exists")

        # Hash password
        hashed_password = ph.hash(password)

        # Create user
        new_user = User(
            name=user_data.name,
            email=email,
            hashedPassword=hashed_password,
            gender=user_data.gender,
        )

        await new_user.insert()

        return new_user
