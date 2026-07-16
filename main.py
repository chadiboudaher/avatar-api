from fastapi import FastAPI, status, HTTPException
from models import CharacterOut, CharacterBase, CharacterCreate
from fake_db import fake_database

app = FastAPI(title="Avatar API")

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/characters", response_model=list[CharacterOut])
async def get_characters():
    return fake_database

@app.get("/characters/{character_id}", response_model=CharacterOut)
async def get_character(character_id: int):
    character = next((item for item in fake_database 
                 if item["id"] == character_id), None)
    if character is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    return character