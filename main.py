from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from sqlalchemy import func

from database import engine, get_db, Base
from models import Character, Nation, User
from schemas import CharacterOut, CharacterCreate, NationOut, UserCreate, UserOut
from auth import hash_password, create_access_token, verify_password
import jwt
from jwt import PyJWTError

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Avatar API")

oauth2_scheme = OAuth2PasswordRequestForm(tokenUrl="login")

@app.exception_handler(Exception)
async def generic_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": "An Unexcepted error occured."})

@app.get("/")
async def root():
    return {"message": "Hello"}

# --------- CREATE DEPENDENCY FOR AUTHORIZED USERS ---------

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
# --------- LOGIN ---------

@app.post("/register", response_model=UserOut,
          status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user: UserCreate,
                   db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username Already taken")
    new_user = User(username=user.username,
                    hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == form_data.username).first()
    if existing is None or not verify_password(form_data.password, existing.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username or password are wrong! Try again")
    token = create_access_token(data={"sub": existing.username})
    return {"access_token": token, "token_type": "bearer"}





# --------- NATION ---------

@app.post("/nations", status_code=status.HTTP_201_CREATED, tags=["Nations"])
async def create_nations(db: Session = Depends(get_db)):
    nation_names = ['water', "earth", "fire", "air"]
    nations = [Nation(name=n) for n in nation_names]
    db.add_all(nations)
    db.commit()
    return None

@app.get("/nations", response_model=list[NationOut], tags=["Nations"])
async def get_nations(db: Session = Depends(get_db)):
    nations = db.query(Nation).all()
    return nations


# --------- CHARACTERS ---------

@app.get("/characters", response_model=list[CharacterOut], tags=["Characters"])
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

@app.get("/characters/{character_id}", response_model=CharacterOut, tags=["Characters"])
async def get_characters(character_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if character is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    return character

@app.post("/characters", response_model=CharacterOut, tags=["Characters"])
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

@app.put("/characters/{character_id}", response_model=CharacterOut, tags=["Characters"])
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

@app.delete("/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Characters"])
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