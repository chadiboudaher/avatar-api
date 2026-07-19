from database import Base
from enums import Show
from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    nation_id: Mapped[int] = mapped_column(ForeignKey("nations.id"))
    nation: Mapped["Nation"] = relationship(back_populates="characters")
    is_bender: Mapped[bool]
    show: Mapped[Show] = mapped_column(SQLEnum(Show))
    first_appearance: Mapped[str] = mapped_column(nullable=True)


class Nation(Base):
    __tablename__ = "nations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    characters: Mapped[list["Character"]] = relationship(back_populates="nation")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]