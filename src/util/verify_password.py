from argon2.exceptions import VerifyMismatchError
from src.util.encode_password import password_hasher


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
