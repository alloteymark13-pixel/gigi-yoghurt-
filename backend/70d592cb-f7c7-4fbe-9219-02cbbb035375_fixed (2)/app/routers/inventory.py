from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/low")
def low_stock(db: Session = Depends(get_db)):
    return crud.list_low_stock(db)
