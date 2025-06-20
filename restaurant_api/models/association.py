"""Модель связывающая блюда и заказы."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from restaurant_api.models.base import BaseModel
from restaurant_api.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from restaurant_api.models import Dish, Order


class OrderDishAssociation(IntIdPkMixin, BaseModel):
    """Модель таблицы с ключами блюд и заказов."""

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        )
    )
    dish_id: Mapped[int] = mapped_column(
        ForeignKey(
            "dishes.id",
            ondelete="RESTRICT",
        )
    )

    # связи
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="dish_associations",
    )
    dish: Mapped["Dish"] = relationship(
        "Dish",
        back_populates="order_associations",
    )
