from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..db import SessionLocal
from ..models import uploads, progress, mock_interviews
from sqlalchemy import select, func

router = APIRouter()

@router.get("/")
def dashboard(current=Depends(get_current_user)):
    db = SessionLocal()
    up = db.execute(select(uploads.c.id, uploads.c.filename, uploads.c.created_at).where(uploads.c.user_id==current["id"]).order_by(uploads.c.created_at.desc()).limit(5)).all()
    pr = db.execute(select(progress.c.id, progress.c.title, progress.c.percent).where(progress.c.user_id==current["id"]).order_by(progress.c.created_at.desc()).limit(5)).all()
    cnt = db.execute(select(func.count()).select_from(mock_interviews).where(mock_interviews.c.user_id==current["id"])).scalar()
    return {"uploads": [dict(row) for row in up], "progress": [dict(row) for row in pr], "interviewsCount": cnt}

