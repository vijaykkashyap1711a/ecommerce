import os
from unittest.mock import Mock

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["API_TOKEN"] = "test-token"
os.environ["PRODUCT_SERVICE_URL"] = "http://product-service"

import pytest
import order_service.app as order_service

app = order_service.app
db = order_service.db


@pytest.fixture()
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_order_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "UP"

    print("\nCheck - Order health endpoint returned UP")


def test_order_requires_token(client):
    response = client.post(
        "/orders",
        json={"product_id": 1, "quantity": 2},
    )

    assert response.status_code == 401

    print("\nCheck - Order creation correctly requires API token")


def test_create_order(client, monkeypatch):
    product_response = Mock()
    product_response.status_code = 200
    product_response.json.return_value = {
        "id": 1,
        "name": "Notebook",
        "price": 100,
        "stock": 5,
    }

    stock_response = Mock()
    stock_response