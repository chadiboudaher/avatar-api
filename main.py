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

@app.post("/characters", response_model=CharacterOut)
async def create_character(new_character: CharacterCreate):
    name_character = next((c for c in
                           fake_database if c['name'] == new_character.name), None)
    if name_character is not None:
        # status 409_CONFLICT can also be used
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Character already exist")
    new_id = max(c["id"] for c in fake_database) + 1
    character_dict = new_character.model_dump()
    character_dict["id"] = new_id
    fake_database.append(character_dict)
    return character_dict

@app.put("/characters/{character_id}", response_model=CharacterOut)
async def update_character(character_id: int,
                           update_character: CharacterCreate):
    index = next((i for i, item in enumerate(fake_database) 
                      if item["id"] == character_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    character_dict = update_character.model_dump()
    character_dict["id"] = character_id
    fake_database[index] = character_dict
    return character_dict

@app.delete("/characters/{character_id}", response_model=CharacterOut)
async def delete_character(character_id: int):
    index = next((i for i, item in enumerate(fake_database)
                  if item["id"] == character_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Character Not Found")
    deleted = fake_database.pop(index)
    return deleted