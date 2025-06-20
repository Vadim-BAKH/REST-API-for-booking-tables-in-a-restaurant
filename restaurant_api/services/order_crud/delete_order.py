"""Удаляет заказ."""

from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.configs import logger
from restaurant_api.exceptions import CannotCancelOrder
from restaurant_api.services.order_crud.order_by_id import get_order_by_id


async def delete_order(
    session: AsyncSession,
    order_id: int,
) -> None:
    """Удаление заказа только со статусом 'в обработке.'"""
    logger.debug(f"Attempting to delete order with id={order_id}")

    order = await get_order_by_id(
        session=session,
        order_id=order_id,
    )

    if order.status != "в обработке":
        logger.warning(
            f"Cannot delete order id={order.id}"
            f" with status='{order.status}'"
        )
        raise CannotCancelOrder()

    await session.delete(order)
    await session.commit()
    logger.info(f"Order deleted successfully (id={order.id})")
