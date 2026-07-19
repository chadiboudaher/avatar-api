from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from enums import Show

class CharacterBase(BaseModel):
    # allows pydantic models to read data from objects attributes
    # Instead of just dictionaries.
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=1, max_length=100)
    bio: Optional[str] = None
    nation_id: int
    is_bender: bool
    show: Show
    first_appearance: Optional[str] = None

class NationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class CharacterCreate(CharacterBase):
    pass

class CharacterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    bio: Optional[str] = None
    nation: NationOut
    is_bender: bool
    show: Show
    first_appearance: Optional[str] = None


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str