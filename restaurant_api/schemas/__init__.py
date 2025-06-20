__all__ = [
    "DishBase",
    "DishRead",
    "DishCreate",
    "OrderBase",
    "OrderRead",
    "OrderCreate",
    "OrderStatusUpdate",
]

from restaurant_api.schemas.dish import DishBase, DishCreate, DishRead
from restaurant_api.schemas.order import (OrderBase, OrderCreate, OrderRead,
                                          OrderStatusUpdate)
