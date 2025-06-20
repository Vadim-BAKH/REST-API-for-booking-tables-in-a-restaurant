"""Тест удаления заказа."""

import pytest
from restaurant_api.exceptions import CannotCancelOrder
from restaurant_api.models import Order
from restaurant_api.services import delete_order
from sqlalchemy import select


@pytest.mark.asyncio
@pytest.mark.order
async def test_delete_order_success(
    db_session,
    sample_order,
):
    """Удаление заказа со статусом 'в обработке' успешно."""

    # sample_order создаётся со статусом "в обработке"
    await delete_order(db_session, sample_order.id)

    # Проверяем, что заказ удалён

    result = await db_session.execute(
        select(Order).where(Order.id == sample_order.id)
    )
    deleted_order = result.scalar_one_or_none()
    assert deleted_order is None


@pytest.mark.asyncio
@pytest.mark.order
async def test_delete_order_cannot_cancel_raises(
    db_session,
    sample_order,
):
    """Попытка удалить заказ со статусом, отличным от 'в обработке'."""

    # Обновляем статус заказа на "готовится"
    sample_order.status = "готовится"
    await db_session.commit()

    with pytest.raises(CannotCancelOrder):
        await delete_order(db_session, sample_order.id)
