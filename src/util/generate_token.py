from datetime import datetime, timedelta, timezone

import jwt

from src.config.config import config


ALGORITHM = "HS256"


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {"sub": user_id, "exp": expire}

    token = jwt.encode(payload, config.secret, algorithm=ALGORITHM)

    return token
