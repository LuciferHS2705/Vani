from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_password_hash, create_access_token, verify_password

router = APIRouter()

@router.post('/register', response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = models.User(email=user_in.email, hashed_password=get_password_hash(user_in.password), full_name=user_in.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/login', response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
