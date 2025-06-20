"""Удаляет блюдо."""

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.configs import logger
from restaurant_api.exceptions import DishIsUsedInOrders
from restaurant_api.models import OrderDishAssociation
from restaurant_api.services.dish_crud.dish_by_id import get_dish_by_id


async def delete_dish(
    session: AsyncSession,
    dish_id: int,
) -> None:
    """Удаляет блюдо не связанное с заказами."""
    logger.debug(f"Attempting to delete dish with id={dish_id}")
    dish = await get_dish_by_id(
        session=session,
        dish_id=dish_id,
    )

    # Проверка: есть ли заказы с этим блюдом
    in_orders = await session.scalar(
        select(exists().where(OrderDishAssociation.dish_id == dish_id))
    )
    if in_orders:
        logger.warning(
            f"Cannot delete dish id={dish_id}, it is used in orders."
        )
        raise DishIsUsedInOrders(dish_id)

    await session.delete(dish)
    await session.commit()
    logger.info(f"Dish deleted: {dish.name} (id={dish.id})")
