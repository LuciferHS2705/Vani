from fastapi import APIRouter, HTTPException, Depends
from ..schemas import SignupIn, LoginIn, UserOut
from ..db import SessionLocal
from ..models import users
from ..utils import auth as auth_utils
from sqlalchemy import select
from fastapi import status

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(payload: SignupIn):
    db = SessionLocal()
    q = select(users).where(users.c.email == payload.email)
    existing = db.execute(q).first()
    if existing:
        raise HTTPException(status_code=409, detail="email already registered")
    pwd = auth_utils.create_password_hash(payload.password)
    ins = users.insert().values(email=payload.email, password_hash=pwd, name=payload.name)
    res = db.execute(ins)
    db.commit()
    user = db.execute(select(users).where(users.c.id == res.inserted_primary_key[0])).first()
    return {"id": user[0].id, "email": user[0].email, "name": user[0].name}

@router.post("/login")
def login(payload: LoginIn):
    db = SessionLocal()
    q = select(users).where(users.c.email == payload.email)
    row = db.execute(q).first()
    if not row:
        raise HTTPException(status_code=401, detail="invalid credentials")
    user = row[0]
    if not auth_utils.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = auth_utils.create_access_token({"uid": user.id, "email": user.email})
    return {"user": {"id": user.id, "email": user.email, "name": user.name}, "token": token}

