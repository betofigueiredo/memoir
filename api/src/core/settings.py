import os

from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

load_dotenv()


class Settings:
    ENV: str = os.environ.get("ENV")
    PORT: int = int(os.environ.get("PORT"))
    DB_URL: str = f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_DB')}/{os.environ.get('POSTGRES_DB')}"
    DB_BASE_MODEL = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
