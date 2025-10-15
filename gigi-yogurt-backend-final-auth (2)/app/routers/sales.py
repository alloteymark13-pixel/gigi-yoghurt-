from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=dict)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    res = crud.create_sale(db, sale.product_id, sale.qty, sale.sale_price)
    if res.get("error"):
        raise HTTPException(status_code=400, detail=res)
    return res

@router.get("/", response_model=list)
def list_sales(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales(db, limit=limit)

@router.get("/summary", response_model=dict)
def sales_summary(db: Session = Depends(get_db)):
    return crud.sales_summary(db)
