"""Тест маршрутов."""

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method, url_template, json_body_func, expected_status",
    [
        # Dishes endpoints
        ("GET", "/api/dishes/", None, 200),
        (
            "POST",
            "/api/dishes/",
            lambda _: {
                "name": "Тестовое блюдо",
                "description": "Описание блюда",
                "price": 150.0,
                "category": "Основные блюда",
            },
            201,
        ),
        ("GET", "/api/dishes/{dish_id}", None, 200),
        ("DELETE", "/api/dishes/{dish_id}", None, 204),
        # Orders endpoints
        ("GET", "/api/orders/", None, 200),
        (
            "POST",
            "/api/orders/",
            lambda dishes: {
                "customer_name": "Иван Иванов",
                "dish_ids": [dish.id for dish in dishes],
            },
            201,
        ),
        ("GET", "/api/orders/{order_id}", None, 200),
        ("DELETE", "/api/orders/{order_id}", None, 204),
        (
            "PATCH",
            "/api/orders/{order_id}/status",
            lambda _: {"status": "готовится"},
            200,
        ),
    ],
)
async def test_api_endpoints(
    client,
    method,
    url_template,
    json_body_func,
    expected_status,
    sample_dishes,
    sample_order,
):
    """Параметризированный тест ручек."""
    # Подставляем id в url, если нужно
    if "{dish_id}" in url_template:
        if not sample_dishes:
            pytest.skip("Нет блюд для проверки эндпоинтов с dish_id")
        url = url_template.format(dish_id=sample_dishes[0].id)
    elif "{order_id}" in url_template:
        if not sample_order:
            pytest.skip("Нет заказов для проверки эндпоинтов с order_id")
        url = url_template.format(order_id=sample_order.id)
    else:
        url = url_template

    # Формируем тело запроса, если функция задана
    json_body = json_body_func(sample_dishes) if json_body_func else None

    if method == "GET":
        response = await client.get(url)
    elif method == "POST":
        response = await client.post(url, json=json_body)
    elif method == "DELETE":
        response = await client.delete(url)
    elif method == "PATCH":
        response = await client.patch(url, json=json_body)
    else:
        pytest.skip(f"Method {method} not поддерживается")

    assert response.status_code == expected_status
