"""Маршруты заказа."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from restaurant_api.database import get_session_db
from restaurant_api.schemas.order import (OrderCreate, OrderRead,
                                          OrderStatusUpdate)
from restaurant_api.services import (create_order, delete_order,
                                     get_all_orders, get_order_by_id,
                                     update_status)

SessionDep = Annotated[
    AsyncSession,
    Depends(get_session_db),
]

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get(
    "/",
    response_model=List[OrderRead],
    status_code=status.HTTP_200_OK,
)
async def read_orders(session: SessionDep):
    """Получение списка всех заказов."""
    return await get_all_orders(session)


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_order(
    data: OrderCreate,
    session: SessionDep,
):
    """Создание нового заказа."""
    return await create_order(session, data)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def read_order(
    order_id: int,
    session: SessionDep,
):
    """Получение заказа по ID."""
    return await get_order_by_id(session, order_id)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_order(
    order_id: int,
    session: SessionDep,
):
    """Удаление заказа со статусом 'в обработке'."""
    await delete_order(session, order_id)


@router.patch(
    "/{order_id}/status",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    session: SessionDep,
):
    """Последовательное обновление статуса заказа."""
    return await update_status(session, order_id, data)
