# Local Development and Testing

## Purpose

This runbook verifies that the complete e-commerce application works locally before cloud deployment. Docker Compose starts PostgreSQL, Product, Order, and Frontend containers on one local Docker network.

## Prerequisites

- Docker and Docker Compose
- Python test virtual environment only for `pytest` commands

Run all commands from the repository root:

```bash
cd /path/to/ecommerce
```

Docker does not require the Python virtual environment. Activate the test environment only when running the Python test suite.

## Start the local environment

Build and start all services:

```bash
docker compose up -d --build
docker compose ps
```

Expected services:

| Service | Expected state | Local port |
| --- | --- | --- |
| `postgres` | Running and healthy | Internal only |
| `product` | Running | `5001` |
| `order` | Running | `5003` |
| `frontend` | Running | `5500` |

Open the dashboard at <http://localhost:5500>.

## Service health checks

```bash
curl -f http://localhost:5001/health
curl -f http://localhost:5003/health
curl -f http://localhost:5500/
```

Each command must return a successful response. The Product and Order health endpoints return a JSON status of `UP`.

## Manual local end-to-end verification

Create a Product:

```bash
curl -X POST http://localhost:5001/products \
  -H "Authorization: Bearer my-demo-token" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":55000,"stock":10}'
```

Create an Order for two units:

```bash
curl -X POST http://localhost:5003/orders \
  -H "Authorization: Bearer my-demo-token" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity":2}'
```

### Expected result

The Product response should confirm that the product was created. The Order response should confirm the order and show a total of `110000.0`. Product stock should reduce from `10` to `8`.

Verify the data directly in PostgreSQL:

```bash
docker compose exec postgres \
  psql -U app -d ecommerce_product_db \
  -c "SELECT * FROM products;"

docker compose exec postgres \
  psql -U app -d ecommerce_order_db \
  -c "SELECT * FROM orders;"
```

The query output should show the updated Product stock and the confirmed Order.

## Automated tests

Activate the test virtual environment, then run the individual suites:

```bash
python -m pytest -s tests/product_unit_test.py
python -m pytest -s tests/order_unit_test.py
python -m pytest -s tests/integration_test.py
```

Run the complete test suite before committing:

```bash
python -m pytest -s tests
```

### Observed test results

| Test file | Coverage demonstrated | Result |
| --- | --- | --- |
| `tests/product_unit_test.py` | Product health, authentication, product creation, and product listing | 4 passed |
| `tests/order_unit_test.py` | Order health, authentication requirement, and order handling | 3 passed |
| `tests/integration_test.py` | Product container health, Order container health, and Product–Order–PostgreSQL integration | 3 passed |

The individually captured suites passed: **10 tests total**.

### Captured test output

```text
((.test-venv) ) vkkashya@VIJAYs-MacBook-Pro ecommerce % python -m pytest -s tests

================================================================================================ test session starts ================================================================================================
platform darwin -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/vkkashya/Desktop/final_ecom/active_local/ecommerce
collected 10 items

tests/integration_test.py
Check- Product container health passed
.
Check- Order container health passed
.
Check- Product, Order, and PostgreSQL integration passed
.

tests/order_unit_test.py
Check - Order health endpoint returned UP
.
Check - Order creation correctly requires API token
..

tests/product_unit_test.py
Check- Product health passed
.
Check- Product authentication passed
.
Check- Product creation passed
.
Check- Product listing passed
.

================================================================================================ 10 passed in 0.34s =================================================================================================
```

## Captured Docker Compose status

```text
((.test-venv) ) vkkashya@VIJAYs-MacBook-Pro ecommerce % docker compose ps

NAME                    IMAGE                 COMMAND                  SERVICE    CREATED          STATUS                    PORTS
ecommerce-frontend-1    ecommerce-frontend    "sh -c 'gunicorn --b…"  frontend   14 seconds ago   Up 3 seconds              5000/tcp, 0.0.0.0:5500->5500/tcp, [::]:5500->5500/tcp
ecommerce-order-1       ecommerce-order       "sh -c 'gunicorn --b…"  order      14 seconds ago   Up 5 seconds              5000/tcp, 0.0.0.0:5003->5003/tcp, [::]:5003->5003/tcp
ecommerce-postgres-1    postgres:16-alpine    "docker-entrypoint.s…"  postgres   15 seconds ago   Up 12 seconds (healthy)   5432/tcp
ecommerce-product-1     ecommerce-product     "sh -c 'gunicorn --b…"  product    14 seconds ago   Up 6 seconds              5000/tcp, 0.0.0.0:5001->5001/tcp, [::]:5001->5001/tcp

((.test-venv) ) vkkashya@VIJAYs-MacBook-Pro ecommerce %
```

This confirms that all four Docker Compose services were running and that PostgreSQL was healthy.

## Deployed API verification

The deployed Product and Order APIs were tested through the application load balancer using Postman.

1. `POST /products` created `Laptop` with price `55000` and stock `10`.
2. `POST /orders` created an order for quantity `2` of that Product.
3. `GET /products/{id}` and `GET /orders/{id}` were used to verify the Product and confirmed Order.
4. `DELETE /products/{id}` removed the test Product after validation.

The captured Product API response returned **201 Created** and showed Product ID `5`, `Laptop`, price `55000.0`, and stock `10`.

## Logs and troubleshooting

```bash
docker compose logs -f product
docker compose logs -f order
docker compose ps
```

If a service fails, first check the PostgreSQL health state and then inspect the affected service logs.

## Cleanup

Stop containers and preserve database data:

```bash
docker compose down
```

Start them again later:

```bash
docker compose up -d
```

Remove containers and the local PostgreSQL volume to reset all data:

```bash
docker compose down -v
```
