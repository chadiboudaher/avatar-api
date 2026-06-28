from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    favorite_nation: str | None = None
    favorite_character: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    favorite_nation: str | None
    favorite_character: str | None
    joined_at: datetime

class CharacterResponse(BaseModel):
    id: int
    name: str
    nation: str
    bending_type: str | None = None
    role: str
    bio: str
    is_avatar: bool