from datetime import datetime, timedelta, timezone
from jose import jwt
import os


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM")
    )
    return encoded_jwt
