"""Тест обновления статуса заказа."""

import pytest
from restaurant_api.exceptions import InvalidOrderStatusChange
from restaurant_api.schemas.order import OrderStatusUpdate
from restaurant_api.services import update_status


@pytest.mark.asyncio
@pytest.mark.order
async def test_update_status_success(
    db_session,
    sample_order,
):
    """Успешное обновление статуса заказа."""
    new_status_data = OrderStatusUpdate(status="готовится")
    updated_order = await update_status(
        db_session, sample_order.id, new_status_data
    )
    assert updated_order.status == "готовится"


@pytest.mark.asyncio
@pytest.mark.order
async def test_update_status_invalid_transition_raises(
    db_session,
    sample_order,
):
    """Попытка некорректного перехода статуса вызывает исключение."""
    invalid_status_data = OrderStatusUpdate(status="доставляется")
    with pytest.raises(InvalidOrderStatusChange):
        await update_status(
            db_session,
            sample_order.id,
            invalid_status_data,
        )


@pytest.mark.asyncio
async def test_order_status_update_invalid_status_value_raises():
    """Проверяем, что Pydantic выбрасывает ошибку при невалидном статусе."""
    with pytest.raises(ValueError):
        OrderStatusUpdate(status="неизвестный статус")
