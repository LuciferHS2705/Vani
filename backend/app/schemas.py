from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupIn(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str]

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]

class ProgressIn(BaseModel):
    title: str
    details: Optional[str] = None
    percent: Optional[int] = 0

class InterviewIn(BaseModel):
    topic: str
    notes: Optional[str] = None
    score: Optional[int] = None

