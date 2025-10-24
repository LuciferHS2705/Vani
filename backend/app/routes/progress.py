from fastapi import APIRouter, Depends, HTTPException
from ..deps import get_current_user
from ..db import SessionLocal
from ..models import progress
from sqlalchemy import select

router = APIRouter()

@router.post("/create")
def create(payload: dict, current=Depends(get_current_user)):
    db = SessionLocal()
    res = db.execute(progress.insert().values(user_id=current["id"], title=payload.get("title"), details=payload.get("details"), percent=payload.get("percent",0)))
    db.commit()
    row = db.execute(select(progress).where(progress.c.id==res.inserted_primary_key[0])).first()
    return {"item": dict(row[0])}

@router.get("/")
def list_progress(current=Depends(get_current_user)):
    db = SessionLocal()
    rows = db.execute(select(progress).where(progress.c.user_id==current["id"]).order_by(progress.c.created_at.desc())).all()
    return {"items": [dict(r[0]) for r in rows]}

@router.post("/update/{id}")
def update(id: int, payload: dict, current=Depends(get_current_user)):
    db = SessionLocal()
    db.execute(progress.update().where(progress.c.id==id).where(progress.c.user_id==current["id"]).values(title=payload.get("title"), details=payload.get("details"), percent=payload.get("percent")))
    db.commit()
    row = db.execute(select(progress).where(progress.c.id==id)).first()
    return {"item": dict(row[0])}

@router.post("/delete/{id}")
def delete(id: int, current=Depends(get_current_user)):
    db = SessionLocal()
    db.execute(progress.delete().where(progress.c.id==id).where(progress.c.user_id==current["id"]))
    db.commit()
    return {"ok": True}

