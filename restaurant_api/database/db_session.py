"""
Модуль конфигурирует асинхронное подключение к базе данных.

PostgreSQL с помощью SQLAlchemy и asyncpg, создаёт движки.
Создаёт фабрики сессий для основной и тестовой БД.
Предоставляет функцию-генератор get_session_db.
"""

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from restaurant_api.db_config import settings

async_engine = create_async_engine(
    url=settings.DB_URL,
    echo=False,
    future=True,
    pool_size=50,
    max_overflow=100,
    connect_args={
        'prepared_statement_name_func': lambda:  f'__asyncpg_{uuid4()}__',
    },
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

