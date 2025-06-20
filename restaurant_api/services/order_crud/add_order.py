"""Создаёт заказ."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from restaurant_api.configs import logger
from restaurant_api.exceptions import DishNotFound
from restaurant_api.models import Dish, Order, OrderDishAssociation
from restaurant_api.schemas.order import OrderCreate, OrderRead


async def create_order(
    session: AsyncSession,
    data: OrderCreate,
) -> OrderRead:
    """Создаёт заказ."""
    logger.debug(
        f"Creating order for customer: {data.customer_name}"
        f" with dish_ids={data.dish_ids}"
    )

    # Проверяем, что все блюда существуют
    result = await session.execute(
        select(Dish).where(Dish.id.in_(data.dish_ids))
    )
    found_dishes = result.scalars().all()

    found_dish_ids = {dish.id for dish in found_dishes}
    missing_ids = set(data.dish_ids) - found_dish_ids
    if missing_ids:
        logger.warning(f"Some dishes not found: {missing_ids}")
        raise DishNotFound(missing_ids)

    # Создаем заказ
    order = Order(
        customer_name=data.customer_name,
        status="в обработке",
    )
    session.add(order)
    await session.flush()  # Получаем order.id

    # Добавляем связи заказ-блюдо
    session.add_all(
        [
            OrderDishAssociation(order_id=order.id, dish_id=dish.id)
            for dish in found_dishes
        ]
    )

    await session.commit()

    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.dish_associations).selectinload(
                OrderDishAssociation.dish
            )
        )
        .where(Order.id == order.id)  # <-- фильтр по id созданного заказа
    )
    order_with_dishes = result.scalars().first()

    logger.info(f"Order created successfully (id={order.id})")
    return OrderRead.model_validate(order_with_dishes)
