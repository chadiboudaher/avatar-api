import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()



def verify_password(plain: str, hashed: str) -> bool:
    return hashed.hash.verify(plain.encode(), hashed.encode())

def create_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)
    data.update({
        "exp": expire
    })
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
