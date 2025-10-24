from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..db import SessionLocal
from ..models import mock_interviews
from sqlalchemy import select

router = APIRouter()

@router.post("/create")
def create(payload: dict, current=Depends(get_current_user)):
    db = SessionLocal()
    res = db.execute(mock_interviews.insert().values(user_id=current["id"], topic=payload.get("topic"), notes=payload.get("notes"), score=payload.get("score")))
    db.commit()
    row = db.execute(select(mock_interviews).where(mock_interviews.c.id==res.inserted_primary_key[0])).first()
    return {"item": dict(row[0])}

@router.get("/")
def list_interviews(current=Depends(get_current_user)):
    db = SessionLocal()
    rows = db.execute(select(mock_interviews).where(mock_interviews.c.user_id==current["id"]).order_by(mock_interviews.c.created_at.desc())).all()
    return {"items": [dict(r[0]) for r in rows]}

