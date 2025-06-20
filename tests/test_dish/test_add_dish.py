"""Тест создания блюда"""

import pytest
from restaurant_api.exceptions import DishAlreadyExists
from restaurant_api.schemas import DishCreate
from restaurant_api.services import create_dish


@pytest.mark.asyncio
@pytest.mark.dish
async def test_create_dish(
    db_session,
    check_name_exists_fn,
):
    """Тестируем создание блюда"""
    dish_name = "Тестовое блюдо"
    description = "Тестовое описание"
    price = 100.55
    category = "Тестовая категория"

    dish_data = DishCreate(
        name=dish_name,
        description=description,
        price=price,
        category=category,
    )

    # Проверяем, что имя свободно
    await check_name_exists_fn(
        db_session,
        dish_name,
    )

    # Создаём блюдо
    created_dish = await create_dish(
        session=db_session,
        data=dish_data,
    )

    assert created_dish.name == dish_name
    assert created_dish.description == description
    assert created_dish.price == price
    assert created_dish.category == category
    assert created_dish.id is not None

    with pytest.raises(DishAlreadyExists):
        await check_name_exists_fn(
            db_session,
            dish_name,
        )
