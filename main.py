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

@app.get("/characters", response_model=list[CharacterOut])
async def get_all(db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    return characters

@app.get("/characters/{character_id}", response_model=CharacterOut)
async def get_characters(character_id: int,
                         db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if character is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    return character

@app.post("/characters", response_model=CharacterOut)
async def create_character(character: CharacterCreate,
                           db: Session = Depends(get_db)):
    new_character = Character(**character.model_dump())
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character