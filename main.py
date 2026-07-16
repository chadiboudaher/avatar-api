from fastapi import FastAPI
from models import CharacterOut, CharacterBase, CharacterCreate
from fake_db import fake_database

app = FastAPI(title="Avatar API")

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/characters", response_model=list[CharacterOut])
async def get_characters():
    return fake_database