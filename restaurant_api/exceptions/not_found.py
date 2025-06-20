"""Модели обработки исключений 'HTTP_404_NOT_FOUND'."""

from fastapi import HTTPException, status


class DishNotFound(HTTPException):
    """Модель исключения 'DishNotFound'."""

    def __init__(self, dish_ids: int | set[int]):
        detail = (
            f"Dish with id {dish_ids} not found"
            if isinstance(dish_ids, int)
            else f"Dishes with ids {sorted(dish_ids)} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class OrderNotFound(HTTPException):
    """Модель исключения 'OrderNotFound'."""

    def __init__(self, order_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found",
        )
