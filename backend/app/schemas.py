from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import Optional
from datetime import date, datetime

class BatchCreate(BaseModel):
    product_id: int
    planned_qty: int

class BatchUpdateComplete(BaseModel):
    actual_qty: int
    total_cost: float

class SaleCreate(BaseModel):
    product_id: int
    qty: int
    sale_price: float

class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    product_id: int
    quantity: int
    price: float
    delivery_date: Optional[date] = None
    notes: Optional[str] = None

class OrderOut(BaseModel):
    order_id: int
    customer_name: str
    phone: str
    product_id: int
    quantity: int
    price: float
    total_amount: float
    status: str
    delivery_date: Optional[date]
    notes: Optional[str]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    is_admin: Optional[bool] = False

class UserOut(BaseModel):
    user_id: int
    username: str
    email: Optional[EmailStr]
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
