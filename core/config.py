from pathlib import Path
import os
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
BASE_URL = "https://fakestoreapi.com"

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):
    api_prefix: str = "/api/v1"
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False

settings = Settings()



