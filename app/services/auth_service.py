from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

def register_user(user: UserCreate, db: Session):
    existing = db.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(user: UserLogin, db: Session):
    db_user = db.exec(select(User).where(User.email == user.email)).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(str(db_user.id))
    return {"access_token": token, "token_type": "bearer"}
