from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
# from sqlalchemy import func

from database import engine, get_db, Base
from models import Character, Nation, User
from schemas import CharacterOut, CharacterCreate, NationOut, UserCreate, UserOut
from auth import hash_password, create_access_token, verify_password, SECRET_KEY, ALGORITHM
import jwt
from jwt import PyJWTError



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Avatar API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.exception_handler(Exception)
async def generic_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": "An Unexpected error occured."})

@app.get("/")
async def root():
    return {"message": "Hello"}

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
