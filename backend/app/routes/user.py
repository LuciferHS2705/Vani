from fastapi import APIRouter, Depends, HTTPException
from ..deps import get_current_user
from ..db import SessionLocal
from ..models import users
from sqlalchemy import select
from ..schemas import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    db = SessionLocal()
    q = select(users).where(users.c.id == current["id"])
    row = db.execute(q).first()
    if not row:
        raise HTTPException(status_code=404, detail="user not found")
    u = row[0]
    return {"id": u.id, "email": u.email, "name": u.name}

@router.post("/update", response_model=UserOut)
def update(payload: dict, current=Depends(get_current_user)):
    db = SessionLocal()
    db.execute(users.update().where(users.c.id == current["id"]).values(name=payload.get("name")))
    db.commit()
    row = db.execute(select(users).where(users.c.id == current["id"])).first()
    u = row[0]
    return {"id": u.id, "email": u.email, "name": u.name}

