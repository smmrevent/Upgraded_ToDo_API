from fastapi import APIRouter, Depends, HTTPException, Response
from config import settings
from schemas import UserCreate, UserOut, UserLogin, TokenCreate
from models import User
from database import Session
from security import hash_password, verify_password, hash_token
import jwt
from datetime import datetime, timedelta, timezone
router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def create_access_token(token: TokenCreate):
    payload = {
        "id": token.id,
        "email": token.email,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return access_token

def create_refresh_token(token: TokenCreate):
    payload = {
        "id": token.id,
        "email": token.email,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    }
    refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return refresh_token

@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(email = user_data.email, hashed_password = hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut(id = new_user.id, email=new_user.email)

@router.post("/login")
def login_user(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    token_data = TokenCreate(id = user.id, email = user.email)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    user.hashed_refresh_token = hash_token(refresh_token)
    db.commit()
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Login successful"}
