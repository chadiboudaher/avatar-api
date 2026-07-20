from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from schemas import CharacterOut, CharacterCreate
from models import Character, Nation, User
from fastapi.security import OAuth2PasswordBearer
from auth import hash_password, create_access_token, verify_password, SECRET_KEY, ALGORITHM
import jwt
from jwt import PyJWTError

router = APIRouter(prefix="/characters", tags=["Characters"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/characters", response_model=list[CharacterOut])
async def get_all(nation: Optional[str] = None,
                  is_bender: Optional[bool] = None,
                  name: Optional[str] = None,
                  skip: int = 0,
                  limit: int = 100,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    query = db.query(Character)
    if nation is not None:
        query = query.join(Nation).filter(Nation.name == nation)
    if is_bender is not None:
        query = query.filter(Character.is_bender == is_bender)
    if name is not None:
        query = query.filter(Character.name.ilike(f"%{name}%"))
    characters = query.offset(skip).limit(limit).all()
    return characters

@router.get("/characters/{character_id}", response_model=CharacterOut)
async def get_characters(character_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if character is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    return character

@router.post("/characters", response_model=CharacterOut)
async def create_character(character: CharacterCreate,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    existing = db.query(Character).filter(Character.name == character.name).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Character Already exists")
    nation = db.query(Nation).filter(Nation.id == character.nation_id).first()
    if nation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Nation Not Found")
    new_character = Character(**character.model_dump())
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character

@router.put("/characters/{character_id}", response_model=CharacterOut)
async def update_character(character_id: int,
                           character: CharacterCreate,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    existing = db.query(Character).filter(Character.id == character_id).first()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    nation = db.query(Nation).filter(Nation.id == character.nation_id).first()
    if nation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Nation Not Found")
    for key, value in character.model_dump().items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(character_id: int,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    existing = db.query(Character).filter(Character.id == character_id).first()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    db.delete(existing)
    db.commit()
    return None