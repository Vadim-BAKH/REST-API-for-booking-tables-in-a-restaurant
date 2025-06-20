"""Схемы для блюд."""

from pydantic import BaseModel, ConfigDict, Field


class DishBase(BaseModel):
    """Базовая модель со всеми полями."""

    name: str = Field(..., max_length=100)
    description: str | None = None
    price: float
    category: str


class DishCreate(DishBase):
    """Модель создания блюда."""

    pass


class DishRead(DishBase):
    """Модель представления блюда."""

    id: int

    model_config = ConfigDict(from_attributes=True)
