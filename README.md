## Project baseline

This project started from the ecommerce-microservices reference implementation
by danakonda. I will reduce the application to three services and add Docker,
Kubernetes, Terraform, AWS CI/CD, automated testing, autoscaling, logging,
and monitoring. source : https://github.com/danakonda/ecommerce-microservices/tree/main

------------
# E-Commerce Microservices

A complete **E-Commerce Microservices application** built using **Python, Flask, PostgreSQL, REST APIs, API Gateway, and a web frontend**.

The project demonstrates how independent microservices communicate with each other and how an API Gateway provides a single entry point for clients.

---

## 🚀 Features

* User Microservice
* Product Microservice
* Order Microservice
* API Gateway
* PostgreSQL database
* RESTful APIs
* API Token Authentication
* Product stock management
* Order creation and validation
* Microservice-to-microservice communication
* Frontend dashboard
* CORS support
* Environment-based configuration
* Git/GitHub ready

---

## 🏗️ Architecture

```text
                         Browser
                            |
                            v
                    Frontend :5500
                            |
                            v
                  API Gateway :5000
                     /      |      \
                    /       |       \
                   v        v        v
             User :5002  Product :5001  Order :5003
                 |           |            |
                 v           v            v
             PostgreSQL  PostgreSQL   PostgreSQL
```

### Order Flow

```text
Client
  |
  v
API Gateway
  |
  v
Order Service
  |
  +----> User Service
  |          |
  |          v
  |      Verify User
  |
  +----> Product Service
             |
             v
         Verify Product
             |
             v
         Check Stock
             |
             v
        Reduce Stock
             |
             v
        Create Order
```

---

## 🛠️ Technologies

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* REST API
* Requests

### Database

* PostgreSQL
* SQLAlchemy ORM

### Authentication

* API Token Authentication
* Bearer Token

### Frontend

* HTML
* CSS
* JavaScript
* Flask

### Development Tools

* Git
* GitHub
* PowerShell
* VS Code

---

## 📁 Project Structure

```text
ecommerce-microservices/
│
├── api_gateway/
│   ├── app.py
│   └── .env
│
├── user_services/
│   ├── app.py
│   └── .env
│
├── product_services/
│   ├── app.py
│   └── .env
│
├── order_service/
│   ├── app.py
│   └── .env
│
├── front_end/
│   ├── app.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── app.js
│       └── styles.css
│
├── .gitignore
├── README.md
└── requirements.txt
```

> `.env` files contain secrets and should not be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-microservices.git
```

```bash
cd ecommerce-microservices
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install Flask Flask-SQLAlchemy psycopg2-binary python-dotenv requests flask-cors
```

---

## 🗄️ PostgreSQL Setup

Create the required PostgreSQL databases:

```sql
CREATE DATABASE ecommerce_user_db;

CREATE DATABASE ecommerce_product_db;

CREATE DATABASE ecommerce_order_db;
```

Configure each service's `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_user_db
API_TOKEN=YOUR_SECRET_TOKEN
```

Use the appropriate database name for each service.

### Product Service

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_product_db
API_TOKEN=YOUR_SECRET_TOKEN
```

### User Service

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_user_db
API_TOKEN=YOUR_SECRET_TOKEN
```

### Order Service

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_order_db
API_TOKEN=YOUR_SECRET_TOKEN

USER_SERVICE_URL=http://localhost:5002
PRODUCT_SERVICE_URL=http://localhost:5001
```

> Never commit real passwords or API tokens to GitHub.

---

## 🔐 Generate API Token

Generate a secure token using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the generated token in your local `.env` files.

---

## ▶️ Running the Application

Start each service in a separate terminal.

### Product Service

```bash
cd product_services
python app.py
```

Runs on:

```text
http://localhost:5001
```

### User Service

```bash
cd user_services
python app.py
```

Runs on:

```text
http://localhost:5002
```

### Order Service

```bash
cd order_service
python app.py
```

Runs on:

```text
http://localhost:5003
```

### API Gateway

```bash
cd api_gateway
python app.py
```

Runs on:

```text
http://localhost:5000
```

### Frontend

```bash
cd front_end
python app.py
```

Runs on:

```text
http://localhost:5500
```

---

# 🔌 API Endpoints

## Users

### Create User

```http
POST /users
```

Example request:

```json
{
    "name": "Raj",
    "email": "raj@gmail.com"
}
```

### Get Users

```http
GET /users
```

### Get User

```http
GET /users/{id}
```

---

## Products

### Create Product

```http
POST /products
```

Example:

```json
{
    "name": "Laptop",
    "price": 55000,
    "stock": 10
}
```

### Get Products

```http
GET /products
```

### Get Product

```http
GET /products/{id}
```

### Update Stock

```http
PUT /products/{id}/stock
```

Example:

```json
{
    "stock": 20
}
```

### Delete Product

```http
DELETE /products/{id}
```

---

## Orders

### Create Order

```http
POST /orders
```

Example:

```json
{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
}
```

### Get Orders

```http
GET /orders
```

### Get Order

```http
GET /orders/{id}
```

Protected endpoints require:

```http
Authorization: Bearer YOUR_SECRET_TOKEN
```

---

# 🧪 Example API Flow

### 1. Create User

```text
POST /users
```

```json
{
    "name": "Raj",
    "email": "raj@gmail.com"
}
```

User ID:

```text
1
```

### 2. Create Product

```text
POST /products
```

```json
{
    "name": "Laptop",
    "price": 55000,
    "stock": 10
}
```

Product ID:

```text
1
```

### 3. Create Order

```text
POST /orders
```

```json
{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
}
```

The system:

1. Checks whether the user exists.
2. Checks whether the product exists.
3. Checks product stock.
4. Calculates total price.
5. Reduces product stock.
6. Creates the order.
7. Stores the order in PostgreSQL.

Example:

```text
Product price = ₹55,000
Quantity      = 2

Total         = ₹110,000
```

Stock:

```text
Before order = 10
Quantity     = 2
After order  = 8
```

---

# 🌐 Frontend

The frontend dashboard is available at:

```text
http://localhost:5500
```

It displays:

* Users
* Products
* Product stock
* Orders
* Order quantity
* Order total
* Order status

---

# 🔒 Security

The project uses Bearer Token authentication for protected APIs.

Example:

```http
Authorization: Bearer YOUR_SECRET_TOKEN
```

Secrets are stored in `.env` files and excluded from Git using `.gitignore`.

For production, this project can be improved with:

* JWT authentication
* Refresh tokens
* HTTPS
* Password hashing
* Role-based access control
* Secret management
* Rate limiting

---

# 📊 Example Result

```text
E-Commerce Dashboard

Users
-------------------------
Raj
ID: 1
Email: raj@gmail.com

Products
-------------------------
Laptop
Price: ₹55,000
Stock: 8

Orders
-------------------------
Order #1
User ID: 1
Product ID: 1
Quantity: 2
Total: ₹110,000
Status: CONFIRMED
```

---

# 🚀 Future Improvements

* Docker and Docker Compose
* JWT authentication
* Redis caching
* RabbitMQ/Kafka messaging
* API documentation with Swagger/OpenAPI
* Unit and integration tests
* CI/CD with GitHub Actions
* Centralized logging
* Monitoring and health checks
* Kubernetes deployment
* Payment service
* Inventory service
* Notification service

---

# 👨‍💻 Author

**Raj**

Python | Flask | PostgreSQL | REST API | Microservices

---

## 📄 License

This project is created for learning and portfolio purposes.

