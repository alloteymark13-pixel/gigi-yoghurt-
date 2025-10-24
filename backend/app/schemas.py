from pydantic import BaseModel, EmailStr
try:
    # Pydantic v2
    from pydantic import ConfigDict  # type: ignore
    HAS_PYDANTIC_V2 = True
except Exception:  # pragma: no cover - fallback for v1
    HAS_PYDANTIC_V2 = False
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

    # Support both Pydantic v1 and v2
    if HAS_PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:
        class Config:  # type: ignore
            orm_mode = True

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

    # Support both Pydantic v1 and v2
    if HAS_PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:
        class Config:  # type: ignore
            orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
