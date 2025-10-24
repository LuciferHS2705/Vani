from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from .core import settings
from .database import engine, Base
from .routers import auth, users, files, ai_proxy

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vani Backend (Netlify)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(ai_proxy.router, prefix="/ai", tags=["ai"])

@app.get("/health")
async def health():
    return {"status": "ok"}

# Netlify adapter
handler = Mangum(app)
