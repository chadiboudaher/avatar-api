from fastapi import FastAPI
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Avatar API")

@app.get("/")
async def root():
    return {
        "message": "The four nations welcome you."
    }