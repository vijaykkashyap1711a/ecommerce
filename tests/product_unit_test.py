import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["API_TOKEN"] = "test-token"

import pytest

from product_services.app import app, db


@pytest.fixture()
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_product_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "UP"

    print("\nCheck- Product health passed")


def test_product_requires_token(client):
    response = client.post(
        "/products",
        json={"name": "Notebook", "price": 100, "stock": 5},
    )

    assert response.status_code == 401

    print("\nCheck- Product authentication passed")


def test_create_product(client):
    response = client.post(
        "/products",
        headers={"Authorization": "Bearer test-token"},
        json={"name": "Notebook", "price": 100, "stock": 5},
    )

    assert response.status_code == 201
    assert response.json["product"]["name"] == "Notebook"

    print("\nCheck- Product creation passed")


def test_list_products(client):
    client.post(
        "/products",
        headers={"Authorization": "Bearer test-token"},
        json={"name": "Notebook", "price": 100, "stock": 5},
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json) == 1

    print("\nCheck- Product listing passed")