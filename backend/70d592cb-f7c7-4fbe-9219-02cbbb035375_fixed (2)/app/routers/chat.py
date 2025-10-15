from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatIn(BaseModel):
    user: str
    message: str

@router.post("/message")
def handle_message(payload: ChatIn, db: Session = Depends(get_db)):
    text = payload.message.lower().strip()
    if text.startswith("create batch"):
        parts = text.split()
        try:
            pid = int(parts[2])
            qty = int(parts[4])
        except:
            return {"reply":"Use: create batch <product_id> qty <n>"}
        b = crud.create_batch(db, pid, qty)
        return {"reply":f"Batch {b.batch_code} created for product {pid} planned {qty}"}
    if "low stock" in text or "what ingredients are low" in text:
        low = crud.list_low_stock(db)
        return {"reply": f"Low stock: {low}"}
    if text.startswith("create order"):
        parts = text.split()
        try:
            customer_name = parts[2]
            phone = parts[3]
            product_id = int(parts[4])
            qty = int(parts[5])
            price = float(parts[6])
        except:
            return {"reply":"Use: create order <name> <phone> <product_id> <qty> <price>"}
        o = crud.create_order(db, {"customer_name":customer_name, "phone":phone, "product_id":product_id, "quantity":qty, "price":price})
        return {"reply":f"Order created: id {o.order_id}, total {o.total_amount}"}
    return {"reply":"Sorry, I didn't understand. Try 'create batch <product_id> qty <n>' or 'create order ...'"}
