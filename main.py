from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Character
from schemas import CharacterOut, CharacterCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Avatar API")

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/characters")
async def get_all(db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    return characters