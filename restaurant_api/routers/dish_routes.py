"""Маршруты блюда."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.database import get_session_db
from restaurant_api.schemas import DishCreate, DishRead
from restaurant_api.services import (create_dish, delete_dish, get_all_dishes,
                                     get_dish_by_id)

router = APIRouter(
    prefix="/dishes",
    tags=["Dishes"],
)

SessionDep = Annotated[
    AsyncSession,
    Depends(get_session_db),
]


@router.get(
    "/",
    response_model=List[DishRead],
    status_code=status.HTTP_200_OK,
)
async def read_all_dishes(
    session: SessionDep,
):
    """Получает все блюда по алфавиту."""
    return await get_all_dishes(session)


@router.get(
    "/{dish_id}",
    response_model=DishRead,
    status_code=status.HTTP_200_OK,
)
async def read_dish(
    dish_id: int,
    session: SessionDep,
):
    """Получает блюдо по-актуальному ID."""
    return await get_dish_by_id(session, dish_id)


@router.post(
    "/",
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_dish(
    dish: DishCreate,
    session: SessionDep,
):
    """Создаёт блюдо с уникальным именем."""
    return await create_dish(session, dish)


@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_dish(
    dish_id: int,
    session: SessionDep,
):
    """Удаляет блюдо не связанное с заказами."""
    await delete_dish(session, dish_id)
