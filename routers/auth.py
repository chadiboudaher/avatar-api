from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import hash_password, create_access_token, verify_password
from models import User
from schemas import UserCreate, UserOut
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserOut,
          status_code=status.HTTP_201_CREATED)
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

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == form_data.username).first()
    if existing is None or not verify_password(form_data.password, existing.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username or password are wrong! Try again")
    token = create_access_token(data={"sub": existing.username})
    return {"access_token": token, "token_type": "bearer"}