"""Тест получает все заказы."""

import pytest
from restaurant_api.models import OrderDishAssociation
from restaurant_api.schemas import OrderRead
from restaurant_api.services import get_all_orders
from sqlalchemy import insert


@pytest.mark.asyncio
@pytest.mark.order
async def test_get_all_orders_empty(db_session):
    """Проверяем, что при пустой базе возвращается пустой список."""
    orders = await get_all_orders(db_session)
    assert isinstance(orders, list)
    assert len(orders) == 0


@pytest.mark.asyncio
@pytest.mark.order
async def test_get_all_orders_with_data(
    db_session,
    sample_order,
    sample_dishes,
):
    """
    Проверяем, что функция возвращает список заказов с блюдами.
    Для этого связываем sample_order с sample_dishes.
    """
    # Связываем блюда с заказом через OrderDishAssociation
    for dish in sample_dishes:
        await db_session.execute(
            insert(OrderDishAssociation).values(
                order_id=sample_order.id,
                dish_id=dish.id,
            )
        )
    await db_session.commit()

    # Получаем все заказы
    orders = await get_all_orders(db_session)

    assert isinstance(orders, list)
    assert len(orders) >= 1  # минимум наш sample_order

    # Проверяем, что наш заказ есть в списке
    order_ids = [order.id for order in orders]
    assert sample_order.id in order_ids

    # Проверяем, что блюда загружены
    order = next(order for order in orders if order.id == sample_order.id)
    assert isinstance(order, OrderRead)
    assert len(order.dishes) == len(sample_dishes)

    # Проверяем, что блюда совпадают по id
    dish_ids_in_order = {dish.id for dish in order.dishes}
    sample_dish_ids = {dish.id for dish in sample_dishes}
    assert dish_ids_in_order == sample_dish_ids
