"""Получает все заказы."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from restaurant_api.configs import logger
from restaurant_api.models import Order, OrderDishAssociation
from restaurant_api.schemas import OrderRead


async def get_all_orders(session: AsyncSession) -> list[OrderRead]:
    """Получает список всех заказов."""
    logger.debug("Fetching all orders from database")

    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.dish_associations).selectinload(
                OrderDishAssociation.dish
            )
        )
        .order_by(Order.id)
    )
    orders = result.scalars().all()

    logger.info(f"Fetched {len(orders)} orders")
    return [OrderRead.model_validate(order) for order in orders]
