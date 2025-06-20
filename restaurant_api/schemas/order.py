"""Схемы для заказов."""

from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from restaurant_api.schemas.dish import DishRead


class OrderBase(BaseModel):
    """Базовая модель заказа с именем клиента."""

    customer_name: str = Field(..., max_length=55)


class OrderCreate(OrderBase):
    """Модель создания заказа со списком ID блюд."""

    dish_ids: List[int]


class OrderRead(OrderBase):
    """Модель получения заказа со всеми полями."""

    id: int
    order_time: datetime
    status: str
    dishes: List[DishRead]  # из association_proxy

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    """Модель для получения статуса заказа."""

    status: Literal[
        "в обработке",
        "готовится",
        "доставляется",
        "доставлен",
    ]
