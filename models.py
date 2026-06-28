from datetime import datetime

from database import Base
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    favorite_nation: Mapped[str | None]
    favorite_character: Mapped[str | None]
    joined_at: Mapped[datetime] = mapped_column(insert_default=func.now())


class Character(Base):
    __tablename__ = "character"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    nation: Mapped[str]
    bending_type: Mapped[str | None]
    role: Mapped[str]
    bio: Mapped[str]
    is_avatar: Mapped[bool]