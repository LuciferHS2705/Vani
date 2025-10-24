from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI + Netlify!"}

@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)
