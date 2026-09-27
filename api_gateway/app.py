from flask import Flask, request, Response
from dotenv import load_dotenv
import requests
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")


def forward_request(url):

    try:

        response = requests.request(
            method=request.method,
            url=url,
            headers={
                key: value
                for key, value in request.headers
                if key.lower() != "host"
            },
            data=request.get_data(),
            params=request.args,
            timeout=10
        )

        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get(
                "Content-Type",
                "application/json"
            )
        )

    except requests.RequestException:

        return {
            "error": "Microservice unavailable"
        }, 503
@app.route(
    "/products",
    methods=["GET", "POST"]
)
def products():

    return forward_request(
        f"{PRODUCT_SERVICE_URL}/products"
    )


@app.route(
    "/products/<int:product_id>",
    methods=["GET", "DELETE"]
)
def product(product_id):

    return forward_request(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    )


@app.route(
    "/products/<int:product_id>/stock",
    methods=["PUT"]
)
def product_stock(product_id):

    return forward_request(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}/stock"
    )

@app.route(
    "/users",
    methods=["GET", "POST"]
)
def users():

    return forward_request(
        f"{USER_SERVICE_URL}/users"
    )

@app.route(
    "/users/<int:user_id>",
    methods=["GET", "DELETE"]
)
def user(user_id):

    return forward_request(
        f"{USER_SERVICE_URL}/users/{user_id}"
    )

@app.route(
    "/orders",
    methods=["GET", "POST"]
)
def orders():

    return forward_request(
        f"{ORDER_SERVICE_URL}/orders"
    )


@app.route(
    "/orders/<int:order_id>",
    methods=["GET"]
)
def order(order_id):

    return forward_request(
        f"{ORDER_SERVICE_URL}/orders/{order_id}"
    )


@app.route("/health")
def health():

    return {
        "service": "api-gateway",
        "status": "UP"
    }


if __name__ == "__main__":

    app.run(
        port=5000,
        debug=True
    )