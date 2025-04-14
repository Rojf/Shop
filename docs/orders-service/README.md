# 📦 Order Service

The Order Service is responsible for order creation, status tracking, and history. It interacts with the Cart, Catalog, Payment, and Notification services.


---

## 🔌 API Endpoints

### POST `/api/v1/orders/`

Creates a new order from the current user's cart.

**Headers:**

```json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "payment_method": "card"
}
```

**Response:**

```json
{
  "order_id": 123,
  "status": "pending",
  "total_price": 99.90
}
```


---

### GET `/api/v1/orders/`

Returns a list of orders for the authenticated user.

**Response:**

```json
[
  {
    "order_id": 123,
    "created_at": "2025-04-10T14:00:00Z",
    "status": "delivered",
    "total_price": 99.90
  },
  ...
]
```


---

### GET `/api/v1/orders/{order_id}/`

Returns detailed information about a specific order.

**Response:**

```json
{
  "order_id": 123,
  "status": "processing",
  "items": [
    {
      "product_id": 42,
      "name": "Wireless Mouse",
      "quantity": 2,
      "price": 25.99
    }
  ],
  "total_price": 51.98,
  "created_at": "2025-04-10T14:00:00Z"
}
```


---

## 📦 Order Status Flow

1. `pending` – created, awaiting payment

2. `processing` – payment confirmed, being prepared

3. `shipped` – sent to customer

4. `delivered` – delivered to customer

5. `canceled` – canceled by user or system


---

## ⚙️ Environment Variables

|Variable|Description|
|---|---|
|`ORDER_DB_HOST`|Hostname of the order database|
|`ORDER_DB_NAME`|PostgreSQL database name|
|`ORDER_DB_USER`|Database user|
|`ORDER_DB_PASSWORD`|Database password|
|`ORDER_NOTIFICATION_URL`|Endpoint to send order status updates|
|`ORDER_PAYMENT_URL`|Endpoint to initiate payment|

---

## 🧪 Testing

```bash
pytest -v src/order/tests/
```


---

## 🛠️ Notes

- Order creation automatically pulls data from the **Cart Service**.

- Payment is handled via the **Payment Service** (e.g. Stripe).

- Notifications are sent via the **Notification Service**.

- Order data is stored in **PostgreSQL**.
