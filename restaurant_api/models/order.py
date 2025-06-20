"""Модель заказа."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from restaurant_api.models.base import BaseModel
from restaurant_api.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from restaurant_api.models import Dish, OrderDishAssociation


class Order(IntIdPkMixin, BaseModel):
    """Модель таблицы с заказами."""

    customer_name: Mapped[str] = mapped_column(
        String(55),
        nullable=False,
    )
    dish_associations: Mapped[list["OrderDishAssociation"]] = relationship(
        "OrderDishAssociation",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    dishes: list["Dish"] = association_proxy(
        "dish_associations",
        "dish",
    )
    order_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    status: Mapped[str] = mapped_column(
        String(55),
        nullable=False,
    )
