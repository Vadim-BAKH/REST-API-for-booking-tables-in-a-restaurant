from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from restaurant_api.db_config import settings


test_async_engine = create_async_engine(settings.TEST_DB_URI)

test_async_session = async_sessionmaker(
    bind=test_async_engine, expire_on_commit=False
)