from restaurant_api.routers.dish_routes import router as dish_router
from restaurant_api.routers.order_routes import router as order_router

__all__ = [
    "dish_router",
    "order_router",
]
