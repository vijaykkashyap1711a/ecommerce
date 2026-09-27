# E-Commerce Microservices Demo

A small Flask and PostgreSQL demonstration with three running applications:

```text
Browser
  |
  +--> Frontend :5500
  |
  +--> Product Service :5001
  |
  +--> Order Service :5003 ----> Product Service :5001
```

The frontend calls the product and order services directly. There is no API
gateway and no user service in this demo.

## Services

- `front_end`: dashboard served on port `5500`
- `product_services`: product CRUD and stock management on port `5001`
- `order_service`: order creation and listing on port `5003`

Product and order services use separate PostgreSQL databases. Protected
operations use the same Bearer token in each service's `.env` file.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the databases:

```sql
CREATE DATABASE ecommerce_product_db;
CREATE DATABASE ecommerce_order_db;
```

Create `product_services/.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_product_db
API_TOKEN=YOUR_SECRET_TOKEN
```

Create `order_service/.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_order_db
API_TOKEN=YOUR_SECRET_TOKEN
PRODUCT_SERVICE_URL=http://localhost:5001
```

The frontend token is configured in `front_end/static/app.js`. Set it to the
same value as `API_TOKEN` before loading protected order data.

## Run

Start these three processes in separate terminals:

```bash
cd product_services && python app.py
cd order_service && python app.py
cd front_end && python app.py
```

Open <http://localhost:5500>.

## API Examples

Create a product:

```http
POST http://localhost:5001/products
Authorization: Bearer YOUR_SECRET_TOKEN
Content-Type: application/json
```

```json
{
  "name": "Laptop",
  "price": 55000,
  "stock": 10
}
```

Create an order:

```http
POST http://localhost:5003/orders
Authorization: Bearer YOUR_SECRET_TOKEN
Content-Type: application/json
```

```json
{
  "product_id": 1,
  "quantity": 2
}
```

When an order is created, the order service checks the product, verifies stock,
reduces stock, calculates the total, and stores the order in PostgreSQL.

## Health Checks

```text
http://localhost:5001/health
http://localhost:5003/health
```
