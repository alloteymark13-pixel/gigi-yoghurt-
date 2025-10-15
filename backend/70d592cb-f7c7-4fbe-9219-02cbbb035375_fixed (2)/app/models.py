from sqlalchemy import Column, Integer, Text, Numeric, TIMESTAMP, ForeignKey, Date, func, String, Boolean
from .db import Base

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    sku = Column(Text, unique=True)
    unit = Column(Text)
    unit_size = Column(Integer)
    shelf_life_days = Column(Integer, default=7)

class Ingredient(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    uom = Column(Text)
    cost_per_uom = Column(Numeric(12,4))
    reorder_point = Column(Numeric(12,4), default=0)

class Recipe(Base):
    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"))
    qty_per_unit = Column(Numeric(12,6))

class Batch(Base):
    __tablename__ = "batches"
    batch_id = Column(Integer, primary_key=True, index=True)
    batch_code = Column(Text, unique=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    planned_qty = Column(Integer)
    actual_qty = Column(Integer)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    status = Column(Text, default="planned")
    total_cost = Column(Numeric(12,4))

class InventoryTx(Base):
    __tablename__ = "inventory_tx"
    tx_id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"))
    quantity = Column(Numeric(12,6))
    tx_type = Column(Text)
    ref = Column(Text)
    timestamp = Column(TIMESTAMP)

class Sale(Base):
    __tablename__ = "sales"
    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    qty = Column(Integer)
    sale_price = Column(Numeric(12,4))
    sale_time = Column(TIMESTAMP, server_default=func.now())

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12,4))
    total_amount = Column(Numeric(12,4))
    status = Column(Text, default="Pending")
    delivery_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=True)
    hashed_password = Column(String(512), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
