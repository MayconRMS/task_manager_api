from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi.security import HTTPBearer

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.services.auth_service import register_user, login_user
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user
