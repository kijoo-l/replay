import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent  # app → backend
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    ENV: str = os.getenv("ENV", "local")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me_later")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    @property
    def is_local(self) -> bool:
        return self.ENV == "local"

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

settings = Settings()
