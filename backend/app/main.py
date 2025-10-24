from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, user, dashboard, progress, interview, uploads
import os

app = FastAPI(title="Vani FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(user.router, prefix="/api/user")
app.include_router(dashboard.router, prefix="/api/dashboard")
app.include_router(progress.router, prefix="/api/progress")
app.include_router(interview.router, prefix="/api/interview")
app.include_router(uploads.router, prefix="/api/uploads")

@app.get("/api/health")
async def health():
    return {"ok": True}

