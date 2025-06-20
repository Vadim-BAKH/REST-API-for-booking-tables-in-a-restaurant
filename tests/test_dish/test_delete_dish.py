"""Тест удаления блюда."""

import pytest
from restaurant_api.exceptions import DishIsUsedInOrders
from restaurant_api.models import Dish, OrderDishAssociation
from restaurant_api.services import delete_dish
from sqlalchemy import insert, select


@pytest.mark.asyncio
@pytest.mark.dish
async def test_delete_dish_success(db_session):
    """Удаляем блюдо не связанное с заказом."""
    dish = Dish(
        name="Каша",
        description="Русская каша",
        price=150.3,
        category="Гарнир",
    )
    db_session.add(dish)
    await db_session.commit()
    await db_session.refresh(dish)

    # Удаляем блюдо (оно не связано с заказами)
    await delete_dish(
        db_session,
        dish.id,
    )

    # Проверяем, что блюда больше нет в базе
    result = await db_session.execute(select(Dish).where(Dish.id == dish.id))
    deleted_dish = result.scalar_one_or_none()
    assert deleted_dish is None


@pytest.mark.asyncio
@pytest.mark.dish
async def test_delete_dish_in_orders_raises(
    db_session,
    sample_dishes,
    sample_order,
):
    """Не удаляется блюдо, связанное с заказом."""

    # Используем первое блюдо из фикстуры sample_dishes
    dish = sample_dishes[0]

    # Добавляем связь с заказом в OrderDishAssociation
    await db_session.execute(
        insert(OrderDishAssociation).values(
            order_id=sample_order.id,
            dish_id=dish.id,
        )
    )
    await db_session.commit()

    # Попытка удалить блюдо должна вызвать исключение
    with pytest.raises(DishIsUsedInOrders):
        await delete_dish(
            db_session,
            dish.id,
        )

    # Проверяем, что блюдо всё ещё в базе
    result = await db_session.execute(select(Dish).where(Dish.id == dish.id))
    existing_dish = result.scalar_one_or_none()
    assert existing_dish is not None
