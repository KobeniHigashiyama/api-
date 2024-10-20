from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.shemas.user import UserCreate, UserInDB
from app.db import models
from app.db.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.security import oauth2_scheme

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
 




@router.get("/me", response_model=UserInDB)
def read_user_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(db, token)
    return current_user

@router.put("/me", response_model=UserInDB)
def update_user_me(user_update: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(db, token)
    current_user.username = user_update.username
    current_user.hashed_password = get_password_hash(user_update.password)
    db.commit()
    db.refresh(current_user)
    return current_user

def get_current_user(db: Session, token: str):
    # Декодирование токена JWT и получение пользователя из базы данных
    # Реализация функции зависит от безопасности
    pass

