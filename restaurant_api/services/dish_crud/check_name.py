"""Проверяет уникальное имя."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.configs import logger
from restaurant_api.exceptions import DishAlreadyExists
from restaurant_api.models import Dish


async def check_name_exists(
    session: AsyncSession,
    dish_name: str,
) -> bool:
    """Проверка уникальности имени."""
    existing_dish = await session.scalar(
        select(Dish).where(Dish.name == dish_name)
    )
    if existing_dish:
        logger.warning(f"Dish with name '{dish_name}' already exists.")
        raise DishAlreadyExists(dish_name)
    logger.debug(f"Dish name '{dish_name}' is available")
    return True
