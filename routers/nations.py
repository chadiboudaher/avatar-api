from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from models import Nation
from schemas import NationOut

router = APIRouter(tags=["Nations"])



@router.post("/nations", status_code=status.HTTP_201_CREATED)
async def create_nations(db: Session = Depends(get_db)):
    nation_names = ['water', "earth", "fire", "air"]
    nations = [Nation(name=n) for n in nation_names]
    db.add_all(nations)
    db.commit()
    return None

@router.get("/nations", response_model=list[NationOut])
async def get_nations(db: Session = Depends(get_db)):
    nations = db.query(Nation).all()
    return nations