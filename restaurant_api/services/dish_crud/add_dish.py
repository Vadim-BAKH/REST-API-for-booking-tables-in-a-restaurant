"""Создаёт блюдо."""

from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.configs import logger
from restaurant_api.models import Dish
from restaurant_api.schemas import DishCreate, DishRead
from restaurant_api.services.dish_crud.check_name import check_name_exists


async def create_dish(
    session: AsyncSession,
    data: DishCreate,
) -> DishRead:
    """Создаёт блюдо с уникальным названием."""
    logger.debug(f"Attempting to create a dish with name: {data.name}")

    await check_name_exists(
        session=session,
        dish_name=data.name,
    )

    new_dish = Dish(**data.model_dump())
    session.add(new_dish)
    await session.commit()
    await session.refresh(new_dish)

    logger.info(
        f"Dish created successfully: {new_dish.name} (id={new_dish.id})"
    )
    return DishRead.model_validate(new_dish)
