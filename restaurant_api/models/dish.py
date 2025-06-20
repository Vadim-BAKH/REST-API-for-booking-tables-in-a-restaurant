"""Модель блюда."""

from typing import TYPE_CHECKING

from sqlalchemy import FLOAT, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from restaurant_api.models.base import BaseModel
from restaurant_api.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from restaurant_api.models import OrderDishAssociation


class Dish(IntIdPkMixin, BaseModel):
    """Модель таблицы с заказами."""

    __tablename__ = "dishes"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default="",
    )
    price: Mapped[float] = mapped_column(
        FLOAT,
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    order_associations: Mapped[list["OrderDishAssociation"]] = relationship(
        "OrderDishAssociation",
        back_populates="dish",
        passive_deletes=True,
    )
