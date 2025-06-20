"""Получает все блюда."""

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.configs import logger
from restaurant_api.models import Dish
from restaurant_api.schemas import DishRead


async def get_all_dishes(session: AsyncSession) -> list[DishRead]:
    """Получает все блюда по алфавиту."""
    logger.debug("Fetching all dishes from the database")

    result: Result = await session.execute(select(Dish).order_by(Dish.name))
    dishes = result.scalars().all()

    logger.info(f"Fetched {len(dishes)} dishes")
    return [DishRead.model_validate(dish) for dish in dishes]
