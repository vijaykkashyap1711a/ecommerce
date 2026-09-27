const API_URL = "http://localhost:5000";

const API_TOKEN ="new token ";


const authHeaders = {
    "Authorization": `Bearer ${API_TOKEN}`,
    "Content-Type": "application/json"
};



async function loadUsers() {

    try {

        const response = await fetch(
            `${API_URL}/users`
        );

        const users = await response.json();

        const container =
            document.getElementById("users");

        container.innerHTML = "";

        if (!Array.isArray(users)) {

            container.innerHTML =
                `<p>Error: ${users.error}</p>`;

            return;
        }

        if (users.length === 0) {

            container.innerHTML =
                "<p>No users found.</p>";

            return;
        }

        users.forEach(user => {

            container.innerHTML += `
                <div class="card">

                    <h3>${user.name}</h3>

                    <p>ID: ${user.id}</p>

                    <p>Email: ${user.email}</p>

                </div>
            `;

        });

    } catch (error) {

        console.error(error);

        document.getElementById("users").innerHTML =
            "<p>Unable to load users.</p>";
    }
}


async function loadProducts() {

    try {

        const response = await fetch(
            `${API_URL}/products`
        );

        const products = await response.json();

        const container =
            document.getElementById("products");

        container.innerHTML = "";

        if (!Array.isArray(products)) {

            container.innerHTML =
                `<p>Error: ${products.error}</p>`;

            return;
        }

        if (products.length === 0) {

            container.innerHTML =
                "<p>No products found.</p>";

            return;
        }

        products.forEach(product => {

            container.innerHTML += `
                <div class="card">

                    <h3>${product.name}</h3>

                    <p>ID: ${product.id}</p>

                    <p>
                        Price: ₹${product.price}
                    </p>

                    <p>
                        Stock: ${product.stock}
                    </p>

                </div>
            `;

        });

    } catch (error) {

        console.error(error);

        document.getElementById("products").innerHTML =
            "<p>Unable to load products.</p>";
    }
}


async function loadOrders() {

    try {

        const response = await fetch(
            `${API_URL}/orders`,
            {
                method: "GET",
                headers: authHeaders
            }
        );

        const orders = await response.json();

        const container =
            document.getElementById("orders");

        container.innerHTML = "";

        if (!response.ok) {

            container.innerHTML =
                `<p>Error: ${orders.error}</p>`;

            return;
        }

        if (!Array.isArray(orders)) {

            container.innerHTML =
                "<p>Invalid order response.</p>";

            return;
        }

        if (orders.length === 0) {

            container.innerHTML =
                "<p>No orders found.</p>";

            return;
        }

        orders.forEach(order => {

            container.innerHTML += `
                <div class="card">

                    <h3>
                        Order #${order.id}
                    </h3>

                    <p>
                        User ID: ${order.user_id}
                    </p>

                    <p>
                        Product ID: ${order.product_id}
                    </p>

                    <p>
                        Quantity: ${order.quantity}
                    </p>

                    <p>
                        Total: ₹${order.total_price}
                    </p>

                    <p>
                        Status: ${order.status}
                    </p>

                </div>
            `;

        });

    } catch (error) {

        console.error(error);

        document.getElementById("orders").innerHTML =
            "<p>Unable to load orders.</p>";
    }
}



window.addEventListener(
    "DOMContentLoaded",
    function () {

        loadUsers();

        loadProducts();

        loadOrders();

    }
);
