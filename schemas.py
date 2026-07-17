from pydantic import BaseModel, ConfigDict
from typing import Optional
from enums import Nation, Show

class CharacterBase(BaseModel):
    # allows pydantic models to read data from objects attributes
    # Instead of just dictionaries.
    model_config = ConfigDict(from_attributes=True)
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