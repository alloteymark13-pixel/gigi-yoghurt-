from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas, models
from ..auth_utils import create_access_token, decode_token
from datetime import timedelta
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "user_id": user.user_id, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    # bootstrap: allow first user if no users exist
    user_count = db.query(models.User).count()
    if user_count > 0:
        if not authorization:
            raise HTTPException(status_code=401, detail="Admin credentials required to create users")
        # Extract token from "Bearer <token>" format
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        payload = decode_token(token)
        if not payload or not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admin privileges required")
    created = crud.create_user(db, user_in.dict())
    if isinstance(created, dict) and created.get("error"):
        raise HTTPException(status_code=400, detail=created["error"])
    return created

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    username = payload["sub"]
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
