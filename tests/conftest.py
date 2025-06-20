"""Конфигуратор тестов."""

from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Coroutine, Type

import pytest
from httpx import ASGITransport, AsyncClient
from restaurant_api.app import app_
from restaurant_api.database import (get_session_db, test_async_engine,
                                     test_async_session)
from restaurant_api.models import Base, Dish, Order
from restaurant_api.services import (check_name_exists, get_dish_by_id,
                                     get_order_by_id)
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
async def override_dependencies():
    """Переопределяет основную сессию на тестовую."""

    async def override_get_db() -> AsyncGenerator[
        AsyncSession,
        None,
    ]:
        """Создает сессию для тестов."""
        async with test_async_session() as session:
            yield session

    app_.dependency_overrides[get_session_db] = override_get_db
    yield
    app_.dependency_overrides.clear()


@pytest.fixture
async def db_session() -> AsyncGenerator[
    AsyncSession,
    None,
]:
    """Возвращает тестовую сессию базы данных."""
    async with test_async_session() as session:
        yield session


@pytest.fixture(autouse=True)
async def test_database() -> AsyncGenerator:
    """Фикстура для управления миграциями."""
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield

    finally:
        async with test_async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_async_engine.dispose()


@pytest.fixture
async def client():
    """Возвращает асинхронный клиент."""
    async with AsyncClient(
        transport=ASGITransport(app=app_), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def get_dish_by_id_fn() -> Callable[
    [AsyncSession, int],
    Coroutine[Any, Any, Type[Dish]],
]:
    """Фикстура для получения блюда по id."""
    return get_dish_by_id


@pytest.fixture
def check_name_exists_fn() -> Callable[
    [AsyncSession, str],
    Coroutine[Any, Any, bool],
]:
    """Фикстура, для проверки уникальности имени блюда."""
    return check_name_exists


@pytest.fixture
def get_order_by_id_fn() -> Callable[
    [AsyncSession, int],
    Coroutine[Any, Any, Type[Order]],
]:
    """Фикстура для получения заказа по id."""
    return get_order_by_id


@pytest.fixture
async def sample_dishes(db_session: AsyncSession):
    """Создаём блюда."""
    dish1 = Dish(
        name="Борщ",
        description="Русский суп",
        price=150.0,
        category="Супы",
    )
    dish2 = Dish(
        name="Пельмени",
        description="Мясные пельмени",
        price=200.0,
        category="Основные блюда",
    )
    dish3 = Dish(
        name="Салат Оливье",
        description="Классический салат",
        price=120.0,
        category="Салаты",
    )
    db_session.add_all([dish1, dish2, dish3])
    await db_session.commit()
    await db_session.refresh(dish1)
    await db_session.refresh(dish2)
    await db_session.refresh(dish3)
    return [dish1, dish2, dish3]


@pytest.fixture
async def sample_order(db_session: AsyncSession):
    """Создаёт и возвращает тестовый заказ в базе."""
    order = Order(
        customer_name="Тестовый клиент",
        order_time=datetime.now(),
        status="в обработке",
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    return order
