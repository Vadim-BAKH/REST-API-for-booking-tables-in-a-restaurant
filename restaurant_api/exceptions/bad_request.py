"""Модели обработки исключений 'HTTP_400_BAD_REQUEST'."""

from fastapi import HTTPException, status


class DishAlreadyExists(HTTPException):
    """Модель исключения 'DishAlreadyExists'."""

    def __init__(self, dish_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dish with name '{dish_name}' already exists",
        )


class DishIsUsedInOrders(HTTPException):
    """Модель исключения 'DishIsUsedInOrders'."""

    def __init__(self, dish_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dish with id {dish_id} is used in existing orders.",
        )


class InvalidOrderStatusChange(HTTPException):
    """Модель исключения 'InvalidOrderStatusChange'."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order status transition",
        )


class CannotCancelOrder(HTTPException):
    """Модель исключения 'CannotCancelOrder'."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only orders in 'в обработке' status can be cancelled",
        )
