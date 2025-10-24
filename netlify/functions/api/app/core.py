from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vani Backend"
    SECRET_KEY: str = "replace_with_secure_random_string"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = "../.env"

settings = Settings()
