from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from .core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = "HS256"

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(subject: str, expires_delta: int | None = None):
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGO)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
        return payload.get("sub")
    except Exception:
        return None
