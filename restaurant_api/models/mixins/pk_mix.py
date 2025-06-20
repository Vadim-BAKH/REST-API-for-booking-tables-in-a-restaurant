"""Модель миксин."""

from sqlalchemy.orm import Mapped, mapped_column


class IntIdPkMixin:
    """Модель определяет общее поле ID."""

    id: Mapped[int] = mapped_column(primary_key=True)
