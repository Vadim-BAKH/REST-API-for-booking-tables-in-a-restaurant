"""Получает блюдо по ID."""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.configs import logger
from restaurant_api.exceptions import DishNotFound
from restaurant_api.models import Dish


async def get_dish_by_id(
    session: AsyncSession,
    dish_id: int,
) -> Type[Dish]:
    """Получает блюдо по актуальному ID."""
    logger.debug(f"Fetching dish by id={dish_id}")
    dish = await session.get(Dish, dish_id)

    if not dish:
        logger.error(f"Dish with id={dish_id} not found")
        raise DishNotFound(dish_id)

    logger.info(f"Dish found: {dish.name} (id={dish.id})")
    return dish
