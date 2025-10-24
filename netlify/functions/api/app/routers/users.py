from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..auth import decode_access_token, get_password_hash

router = APIRouter()

def get_current_user(db: Session = Depends(database.get_db), authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization')
    scheme, _, token = authorization.partition(' ')
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid token')
    user = db.query(models.User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.get('/me', response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.patch('/me', response_model=schemas.UserOut)
def update_me(update: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if update.full_name:
        current_user.full_name = update.full_name
    if update.password:
        current_user.hashed_password = get_password_hash(update.password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
