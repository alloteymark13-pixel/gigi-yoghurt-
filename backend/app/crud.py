from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from sqlalchemy import func
from .auth_utils import get_password_hash, verify_password

def create_batch(db: Session, product_id: int, planned_qty: int):
    code = f"B-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    b = models.Batch(batch_code=code, product_id=product_id, planned_qty=planned_qty, status="planned")
    db.add(b)
    db.commit()
    db.refresh(b)
    return b

def start_batch(db: Session, batch_id: int):
    b = db.query(models.Batch).filter(models.Batch.batch_id==batch_id).first()
    if not b:
        return None
    b.status = "in_production"
    b.start_time = datetime.utcnow()
    db.commit()
    db.refresh(b)
    return b

def complete_batch(db: Session, batch_id: int, actual_qty:int, total_cost:float):
    b = db.query(models.Batch).filter(models.Batch.batch_id==batch_id).first()
    if not b:
        return None
    b.status = "completed"
    b.end_time = datetime.utcnow()
    b.actual_qty = actual_qty
    b.total_cost = total_cost
    db.commit()
    db.refresh(b)
    return b

def list_low_stock(db: Session):
    rows = db.query(models.Ingredient, func.coalesce(func.sum(models.InventoryTx.quantity),0).label("qty_on_hand"))\
        .outerjoin(models.InventoryTx, models.Ingredient.ingredient_id==models.InventoryTx.ingredient_id)\
        .group_by(models.Ingredient.ingredient_id).all()
    low = []
    for ing, qty in rows:
        if qty <= ing.reorder_point:
            low.append({"ingredient_id":ing.ingredient_id, "name":ing.name, "qty_on_hand":float(qty), "reorder_point":float(ing.reorder_point)})
    return low

def compute_batch_cost(db: Session, product_id: int, planned_qty: int):
    q = db.query(models.Recipe, models.Ingredient)\
        .join(models.Ingredient, models.Recipe.ingredient_id==models.Ingredient.ingredient_id)\
        .filter(models.Recipe.product_id==product_id).all()
    if not q:
        return {"error":"No recipe found for product"}
    breakdown = []
    total_cost = 0.0
    for recipe, ing in q:
        needed = float(recipe.qty_per_unit) * float(planned_qty)
        cost = needed * float(ing.cost_per_uom or 0)
        breakdown.append({"ingredient_id": ing.ingredient_id, "name": ing.name, "needed": needed, "unit": ing.uom, "unit_cost": float(ing.cost_per_uom or 0), "cost": round(cost,4)})
        total_cost += cost
    return {"product_id":product_id, "planned_qty":planned_qty, "total_cost": round(total_cost,4), "breakdown": breakdown}

def get_qty_on_hand(db: Session, ingredient_id: int):
    qty = db.query(func.coalesce(func.sum(models.InventoryTx.quantity),0)).filter(models.InventoryTx.ingredient_id==ingredient_id).scalar()
    return float(qty or 0.0)

def reserve_ingredients_for_batch(db: Session, batch_id: int):
    batch = db.query(models.Batch).filter(models.Batch.batch_id==batch_id).first()
    if not batch:
        return {"error":"Batch not found"}
    recipes = db.query(models.Recipe, models.Ingredient)\
        .join(models.Ingredient, models.Recipe.ingredient_id==models.Ingredient.ingredient_id)\
        .filter(models.Recipe.product_id==batch.product_id).all()
    if not recipes:
        return {"error":"No recipe found for product"}
    needed_list = []
    for recipe, ing in recipes:
        needed = float(recipe.qty_per_unit) * float(batch.planned_qty)
        needed_list.append((ing, needed))
    for ing, needed in needed_list:
        qty_on_hand = get_qty_on_hand(db, ing.ingredient_id)
        if qty_on_hand < needed:
            return {"error":"insufficient_stock", "ingredient": ing.name, "needed": needed, "on_hand": qty_on_hand}
    txs = []
    try:
        for ing, needed in needed_list:
            tx = models.InventoryTx(ingredient_id=ing.ingredient_id, quantity=-needed, tx_type="OUT", ref=f"reserve_batch_{batch.batch_code}", timestamp=datetime.utcnow())
            db.add(tx)
            db.flush()
            txs.append({"ingredient_id":ing.ingredient_id, "name":ing.name, "quantity": -needed, "tx_id": tx.tx_id})
        batch.status = "reserved"
        db.commit()
        db.refresh(batch)
    except Exception as e:
        db.rollback()
        return {"error":"reservation_failed", "detail": str(e)}
    return {"ok": True, "transactions": txs}

def available_units_for_product(db: Session, product_id: int) -> int:
    produced = db.query(func.coalesce(func.sum(models.Batch.actual_qty), 0))\
                 .filter(models.Batch.product_id == product_id, models.Batch.status == 'completed')\
                 .scalar()
    sold = db.query(func.coalesce(func.sum(models.Sale.qty), 0))\
             .filter(models.Sale.product_id == product_id).scalar()
    produced_val = int(float(produced or 0))
    sold_val = int(float(sold or 0))
    return produced_val - sold_val

def create_sale(db: Session, product_id: int, qty: int, sale_price: float):
    available = available_units_for_product(db, product_id)
    if available < qty:
        return {"error": "insufficient_finished_goods", "available": available, "requested": qty}
    s = models.Sale(product_id=product_id, qty=qty, sale_price=sale_price)
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"ok": True, "sale_id": s.sale_id, "product_id": product_id, "qty": qty, "sale_price": float(s.sale_price), "sale_time": str(s.sale_time)}

def get_sales(db: Session, limit: int = 100):
    rows = db.query(models.Sale, models.Product)\
             .join(models.Product, models.Sale.product_id == models.Product.product_id)\
             .order_by(models.Sale.sale_time.desc())\
             .limit(limit).all()
    out = []
    for sale, prod in rows:
        out.append({
            "sale_id": sale.sale_id,
            "product_id": sale.product_id,
            "product_name": prod.name,
            "qty": int(sale.qty),
            "sale_price": float(sale.sale_price),
            "sale_time": sale.sale_time.isoformat() if sale.sale_time else None
        })
    return out

def sales_summary(db: Session):
    rows = db.query(
                models.Product.name.label("product"),
                func.coalesce(func.sum(models.Sale.qty), 0).label("units_sold"),
                func.coalesce(func.sum(models.Sale.qty * models.Sale.sale_price), 0).label("revenue")
            ) \
            .outerjoin(models.Sale, models.Product.product_id == models.Sale.product_id) \
            .group_by(models.Product.name) \
            .all()

    by_product = []
    total_units = 0
    total_revenue = 0.0
    for product, units_sold, revenue in rows:
        units = int(units_sold or 0)
        rev = float(revenue or 0.0)
        by_product.append({"product": product, "units_sold": units, "revenue": round(rev, 4)})
        total_units += units
        total_revenue += rev

    return {"total_units": total_units, "total_revenue": round(total_revenue, 4), "by_product": by_product}

def create_order(db: Session, order_data):
    price = float(order_data.get("price", 0))
    qty = int(order_data.get("quantity", 1))
    total = round(price * qty, 4)
    o = models.Order(
        customer_name=order_data["customer_name"],
        phone=order_data["phone"],
        product_id=order_data["product_id"],
        quantity=qty,
        price=price,
        total_amount=total,
        status=order_data.get("status", "Pending"),
        delivery_date=order_data.get("delivery_date", None),
        notes=order_data.get("notes", None)
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    return o

def get_orders(db: Session, limit: int = 200):
    rows = db.query(models.Order).order_by(models.Order.created_at.desc()).limit(limit).all()
    return rows

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.order_id==order_id).first()

def update_order(db: Session, order_id: int, updates: dict):
    o = db.query(models.Order).filter(models.Order.order_id==order_id).first()
    if not o:
        return None
    for k,v in updates.items():
        if hasattr(o, k):
            setattr(o, k, v)
    db.commit()
    db.refresh(o)
    return o

def delete_order(db: Session, order_id: int):
    o = db.query(models.Order).filter(models.Order.order_id==order_id).first()
    if not o:
        return False
    db.delete(o)
    db.commit()
    return True

# USER helpers
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user_create):
    if get_user_by_username(db, user_create.get("username")):
        return {"error":"username_exists"}
    hashed = get_password_hash(user_create.get("password"))
    user = models.User(
        username = user_create.get("username"),
        email = user_create.get("email"),
        hashed_password = hashed,
        is_admin = user_create.get("is_admin", False),
        is_active = True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
