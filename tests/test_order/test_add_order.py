"""Тест создания заказа."""

import pytest
from restaurant_api.exceptions import DishNotFound
from restaurant_api.schemas.order import OrderCreate
from restaurant_api.services import create_order


@pytest.mark.asyncio
@pytest.mark.order
async def test_create_order_success(
    db_session,
    sample_dishes,
):
    """Успешное создание заказа с существующими блюдами."""

    dish_ids = [
        dish.id for dish in sample_dishes[:2]
    ]  # берем первые два блюда
    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dish_ids=dish_ids,
    )

    order_read = await create_order(
        db_session,
        order_data,
    )

    assert order_read.customer_name == order_data.customer_name
    assert order_read.status == "в обработке"
    assert len(order_read.dishes) == len(dish_ids)
    returned_dish_ids = {dish.id for dish in order_read.dishes}
    assert set(dish_ids) == returned_dish_ids


@pytest.mark.asyncio
@pytest.mark.order
async def test_create_order_with_missing_dish_raises(
    db_session, sample_dishes
):
    """Создание заказа с несуществующим id блюда."""
    existing_dish_ids = [dish.id for dish in sample_dishes[:1]]
    missing_dish_id = 999999  # явно несуществующий id
    dish_ids = existing_dish_ids + [missing_dish_id]

    order_data = OrderCreate(
        customer_name="Пётр Петров",
        dish_ids=dish_ids,
    )

    with pytest.raises(DishNotFound) as exc_info:
        await create_order(db_session, order_data)

    assert missing_dish_id in exc_info.value.args[0]
