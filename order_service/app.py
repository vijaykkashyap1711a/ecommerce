from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from functools import wraps
import requests
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

API_TOKEN = os.getenv("API_TOKEN")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="CONFIRMED"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_price": float(self.total_price),
            "status": self.status
        }


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": "Authorization header required"
            }), 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({
                "error": "Invalid Authorization format"
            }), 401

        if parts[1] != API_TOKEN:
            return jsonify({
                "error": "Invalid API token"
            }), 401

        return f(*args, **kwargs)

    return decorated

@app.route("/orders", methods=["POST"])
@token_required
def create_order():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body required"
        }), 400

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not user_id or not product_id or not quantity:
        return jsonify({
            "error": "user_id, product_id and quantity are required"
        }), 400

    if quantity <= 0:
        return jsonify({
            "error": "Quantity must be greater than 0"
        }), 400



    try:

        user_response = requests.get(
            f"{USER_SERVICE_URL}/users/{user_id}",
            timeout=5
        )

    except requests.RequestException:

        return jsonify({
            "error": "User service unavailable"
        }), 503

    if user_response.status_code == 404:

        return jsonify({
            "error": "User does not exist"
        }), 404

    if user_response.status_code != 200:

        return jsonify({
            "error": "Unable to validate user"
        }), 503
    try:

        product_response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}",
            timeout=5
        )

    except requests.RequestException:

        return jsonify({
            "error": "Product service unavailable"
        }), 503

    if product_response.status_code == 404:

        return jsonify({
            "error": "Product does not exist"
        }), 404

    if product_response.status_code != 200:

        return jsonify({
            "error": "Unable to validate product"
        }), 503

    product = product_response.json()
    if product["stock"] < quantity:

        return jsonify({
            "error": "Insufficient stock",
            "available_stock": product["stock"]
        }), 400
    total_price = product["price"] * quantity
    new_stock = product["stock"] - quantity

    try:

        stock_response = requests.put(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}/stock",
            headers={
                "Authorization": f"Bearer {API_TOKEN}"
            },
            json={
                "stock": new_stock
            },
            timeout=5
        )

    except requests.RequestException:

        return jsonify({
            "error": "Unable to update product stock"
        }), 503

    if stock_response.status_code != 200:

        return jsonify({
            "error": "Stock update failed"
        }), 500

    # -----------------------------
    # Create Order
    # -----------------------------

    order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total_price,
        status="CONFIRMED"
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        "message": "Order created successfully",
        "order": order.to_dict()
    }), 201

@app.route("/orders", methods=["GET"])
@token_required
def get_orders():

    orders = Order.query.all()

    return jsonify([
        order.to_dict()
        for order in orders
    ])
@app.route("/orders/<int:order_id>", methods=["GET"])
@token_required
def get_order(order_id):

    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order.to_dict())


@app.route("/health")
def health():

    return jsonify({
        "service": "order-service",
        "status": "UP"
    })


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(port=5003, debug=True)