"""Обновление статуса заказа."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from restaurant_api.configs import logger
from restaurant_api.exceptions import InvalidOrderStatusChange
from restaurant_api.models import Order, OrderDishAssociation
from restaurant_api.schemas import OrderRead
from restaurant_api.schemas.order import OrderStatusUpdate
from restaurant_api.services.order_crud.order_by_id import get_order_by_id

ORDER_STATUSES = [
    "в обработке",
    "готовится",
    "доставляется",
    "доставлен",
]


async def update_status(
    session: AsyncSession,
    order_id: int,
    data: OrderStatusUpdate,
) -> OrderRead:
    """Последовательно обновляет статус заказа."""
    new_status = data.status
    logger.debug(f"Updating status for order #{order_id} → '{new_status}'")

    order = await get_order_by_id(
        session=session,
        order_id=order_id,
    )

    try:
        current_index = ORDER_STATUSES.index(order.status)
        new_index = ORDER_STATUSES.index(new_status)
    except ValueError:
        logger.error(
            f"Invalid status transition value:"
            f" '{order.status}' → '{new_status}'."
        )
        raise InvalidOrderStatusChange()

    if new_index != current_index + 1:
        logger.warning(
            f"Invalid status transition attempt:"
            f" {order.status} → {new_status}"
        )
        raise InvalidOrderStatusChange()

    order.status = new_status
    await session.commit()

    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.dish_associations).selectinload(
                OrderDishAssociation.dish
            )
        )
        .where(Order.id == order.id)
    )
    order_with_dishes = result.scalars().first()

    logger.info(f"Order #{order.id} status changed to '{new_status}'")
    return OrderRead.model_validate(order_with_dishes)
