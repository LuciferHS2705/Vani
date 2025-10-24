from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..deps import get_current_user
from ..db import SessionLocal
from ..models import uploads
from supabase import create_client
import os, uuid

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET = os.getenv("SUPABASE_BUCKET", "vani-uploads")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL and SUPABASE_KEY required for uploads route")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

@router.post("/")
def upload(file: UploadFile = File(...), current=Depends(get_current_user)):
    contents = file.file.read()
    filename = f"{current['id']}/{uuid.uuid4().hex}_{file.filename}"
    res = supabase.storage.from_(BUCKET).upload(filename, contents)
    if res.get("error"):
        raise HTTPException(status_code=500, detail="upload failed: " + str(res["error"]))
    public_url = supabase.storage.from_(BUCKET).get_public_url(filename).get("publicURL")
    db = SessionLocal()
    info = db.execute(uploads.insert().values(user_id=current["id"], filename=file.filename, mime=file.content_type, supabase_path=filename))
    db.commit()
    row = db.execute(select(uploads).where(uploads.c.id==info.inserted_primary_key[0])).first()
    return {"item": dict(row[0]), "public_url": public_url}

@router.get("/")
def list_uploads(current=Depends(get_current_user)):
    db = SessionLocal()
    rows = db.execute(select(uploads).where(uploads.c.user_id==current["id"]).order_by(uploads.c.created_at.desc())).all()
    return {"items": [dict(r[0]) for r in rows]}

from fastapi.responses import StreamingResponse
from sqlalchemy import select
@router.get("/{id}")
def download(id: int, current=Depends(get_current_user)):
    db = SessionLocal()
    row = db.execute(select(uploads).where(uploads.c.id==id).where(uploads.c.user_id==current["id"])).first()
    if not row:
        raise HTTPException(status_code=404, detail="not found")
    rec = row[0]
    data = supabase.storage.from_(BUCKET).download(rec.supabase_path)
    if data.get("error"):
        raise HTTPException(status_code=500, detail="download failed")
    content = data.get("data")
    return StreamingResponse(content, media_type=rec.mime)

