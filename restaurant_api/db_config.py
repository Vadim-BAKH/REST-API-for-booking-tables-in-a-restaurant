from os import getenv

from dotenv import load_dotenv


class Settings:
    load_dotenv()
    POSTGRES_USER = getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
    DB_PORT = getenv("DB_PORT")
    POSTGRES_DB = getenv("POSTGRES_DB")

    DB_URI = \
        (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
         f"@db:{DB_PORT}/{POSTGRES_DB}")

    TEST_DB_URI = "postgresql+asyncpg://test:test@localhost:5433/test_db"

settings = Settings()
