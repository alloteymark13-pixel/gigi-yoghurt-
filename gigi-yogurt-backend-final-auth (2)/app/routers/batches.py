from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas
from ..auth_utils import decode_token

router = APIRouter(prefix="/batches", tags=["batches"])

@router.post("/", response_model=dict)
def create_batch(batch: schemas.BatchCreate, db: Session = Depends(get_db)):
    b = crud.create_batch(db, batch.product_id, batch.planned_qty)
    return {"batch_id": b.batch_id, "batch_code": b.batch_code, "planned_qty": b.planned_qty, "status":b.status}

@router.post("/{batch_id}/start", response_model=dict)
def start_batch(batch_id: int, db: Session = Depends(get_db)):
    b = crud.start_batch(db, batch_id)
    if not b:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"batch_id": b.batch_id, "status": b.status, "start_time": b.start_time}

@router.post("/{batch_id}/complete", response_model=dict)
def complete_batch(batch_id: int, payload: schemas.BatchUpdateComplete, db: Session = Depends(get_db)):
    b = crud.complete_batch(db, batch_id, payload.actual_qty, payload.total_cost)
    if not b:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"batch_id": b.batch_id, "status": b.status, "actual_qty": b.actual_qty, "total_cost": float(b.total_cost)}
