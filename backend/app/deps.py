from fastapi import Header, HTTPException, Depends
from .utils import auth as auth_utils
from .db import SessionLocal
from sqlalchemy import select
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing authorization header")
    parts = authorization.split(" ")
    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="bad authorization header")
    token = parts[1]
    payload = auth_utils.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="invalid token")
    db = SessionLocal()
    q = select("users").where()  # placeholder not used
    return {"id": payload.get("uid"), "email": payload.get("email")}

