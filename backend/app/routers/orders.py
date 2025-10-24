from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    o = crud.create_order(db, order.dict())
    return o

@router.get("/", response_model=list)
def list_orders(limit: int = 200, db: Session = Depends(get_db)):
    rows = crud.get_orders(db, limit=limit)
    return rows

@router.get("/dashboard", response_model=dict)
def dashboard(db: Session = Depends(get_db)):
    rows = crud.get_orders(db, limit=10000)
    total_orders = len(rows)
    status_counts = {"Pending":0, "In Progress":0, "Delivered":0, "Cancelled":0}
    total_revenue = 0.0
    for o in rows:
        st = o.status or "Pending"
        status_counts.setdefault(st,0)
        status_counts[st] += 1
        total_revenue += float(o.total_amount or 0)
    avg = round(total_revenue / total_orders, 2) if total_orders else 0.0
    return {
        "total_orders": total_orders,
        "pending_orders": status_counts.get("Pending",0),
        "in_progress_orders": status_counts.get("In Progress",0),
        "delivered_orders": status_counts.get("Delivered",0),
        "cancelled_orders": status_counts.get("Cancelled",0),
        "total_revenue": round(total_revenue,2),
        "average_order_value": avg
    }

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = crud.get_order(db, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o

@router.put("/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int, order_updates: dict, db: Session = Depends(get_db)):
    o = crud.update_order(db, order_id, order_updates)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o

@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_order(db, order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}
