"""Получает заказ по id."""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from restaurant_api.configs import logger
from restaurant_api.exceptions import OrderNotFound
from restaurant_api.models import Order, OrderDishAssociation


async def get_order_by_id(
    session: AsyncSession,
    order_id: int,
) -> Type[Order]:
    """Получение заказа по id/"""
    logger.debug(f"Fetching order by id={order_id}")

    order = await session.get(
        Order,
        order_id,
        options=[
            selectinload(Order.dish_associations).selectinload(
                OrderDishAssociation.dish
            )
        ],
    )

    if not order:
        logger.error(f"Order with id={order_id} not found")
        raise OrderNotFound(order_id)

    logger.info(f"Order found: (id={order.id})")
    return order
