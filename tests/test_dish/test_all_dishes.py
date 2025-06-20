"""Тест получения всех блюд"""

import pytest
from restaurant_api.services import get_all_dishes


@pytest.mark.asyncio
@pytest.mark.dish
async def test_get_all_dishes_empty(db_session):
    """Тестируем получение блюд из пустой базы."""
    dishes = await get_all_dishes(db_session)
    assert isinstance(dishes, list)
    assert len(dishes) == 0


@pytest.mark.asyncio
@pytest.mark.dish
async def test_get_all_dishes_with_data(
    db_session,
    sample_dishes,
):
    """Тестируем получение списка блюд с данными."""

    dishes = await get_all_dishes(db_session)

    # Проверяем, что вернулся список с нужным количеством блюд
    assert isinstance(dishes, list)
    assert len(dishes) == len(sample_dishes)
