from pydantic import BaseModel
from typing import Optional, Annotated
from enum import Enum

class Nation(Enum):
    EARTH = "earth"
    WATER = "water"
    FIRE = "fire"
    AIR = "air"

class Show(Enum):
    ATLA = "Avatar The Last Airbender"
    LOK = "Legend of Korra"

class CharacterBase(BaseModel):
    name: str
    bio: Optional[str] = None
    nation: Nation
    is_bender: bool
    show: Show
    first_appearance: Optional[str] = None

class CharacterCreate(CharacterBase):
    pass

class CharacterOut(CharacterBase):
    id: int
