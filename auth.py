import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict,
                        expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)