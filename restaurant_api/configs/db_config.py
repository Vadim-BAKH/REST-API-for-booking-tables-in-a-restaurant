"""Конфигуратор базы данных."""

from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Модель базы данных."""

    POSTGRES_USER = getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
    DB_PORT = getenv("DB_PORT")
    POSTGRES_DB = getenv("POSTGRES_DB")
    DB_HOST = getenv("DB_HOST", "localhost")

    DB_URI = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    )

    TEST_DB_URI = "postgresql+asyncpg://test:test@localhost:5433/test_db"


settings = Settings()
