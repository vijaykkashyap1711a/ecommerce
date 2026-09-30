import uuid

import requests


API_TOKEN = "my-demo-token"
PRODUCT_URL = "http://localhost:5001"
ORDER_URL = "http://localhost:5003"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


def test_product_health():
    response = requests.get(f"{PRODUCT_URL}/health", timeout=5)

    assert response.status_code == 200
    assert response.json()["status"] == "UP"

    print("\nCheck- Product container health passed")


def test_order_health():
    response = requests.get(f"{ORDER_URL}/health", timeout=5)

    assert response.status_code == 200
    assert response.json()["status"] == "UP"

    print("\nCheck- Order container health passed")


def test_create_product_and_order():
    product_name = f"Test Notebook {uuid.uuid4().hex[:8]}"

    product_response = requests.post(
        f"{PRODUCT_URL}/products",
        headers=HEADERS,
        json={"name": product_name, "price": 100, "stock": 5},
        timeout=5,
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["product"]["id"]

    order_response = requests.post(
        f"{ORDER_URL}/orders",
        headers=HEADERS,
        json={"product_id": product_id, "quantity": 2},
        timeout=5,
    )

    assert order_response.status_code == 201
    assert order_response.json()["order"]["total_price"] == 200.0

    product_response = requests.get(
        f"{PRODUCT_URL}/products/{product_id}",
        timeout=5,
    )

    assert product_response.status_code == 200
    assert product_response.json()["stock"] == 3

    print("\nCheck- Product, Order, and PostgreSQL integration passed")