from database import Base
from enums import Nation, Show
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    nation: Mapped[Nation] = mapped_column(SQLEnum(Nation))
    is_bender: Mapped[bool]
    show: Mapped[Show] = mapped_column(SQLEnum(Show))
    first_appearance: Mapped[str] = mapped_column(nullable=True)