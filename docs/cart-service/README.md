# 🛒 Cart Service

The Cart Service manages the shopping cart functionality — adding, updating, removing products, and retrieving the user's cart.

---

## 🔌 API Endpoints

### GET `/api/v1/cart/`

Returns the current user's cart with all items.

**Headers:**

```json
Authorization: Bearer <token>
```


**Response:**

```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 42,
      "product_name": "Wireless Mouse",
      "quantity": 2,
      "price_per_item": 25.99
    }
  ],
  "total_price": 51.98
}
```


---

### POST `/api/v1/cart/add`

Adds an item to the cart or updates the quantity if it already exists.

**Request Body:**

```json
{
  "product_id": 42,
  "quantity": 1
}
```

**Response:**

```json
{
  "message": "Item added to cart"
}
```


---

### POST `/api/v1/cart/remove`

Removes an item from the cart.

**Request Body:**

```json
{
  "product_id": 42
}
```

**Response:**

```json
{
  "message": "Item removed from cart"
}
```


---


### POST `/api/v1/cart/clear`

Clears the entire cart for the current user.

**Response:**

```json
{
  "message": "Cart cleared"
}
```


---


## ⚙️ Environment Variables

|Variable|Description|
|---|---|
|`CART_REDIS_HOST`|Redis host for storing cart data|
|`CART_REDIS_PORT`|Redis port|
|`CART_EXPIRE_TIME`|Optional TTL for cart (in seconds)|

---


## 🧪 Testing

Run unit tests for the cart service with:

```bash
pytest -v src/cart/tests/
```


---

## 🛠️ Implementation Notes

- Cart data is stored in **Redis** for fast access.

- Each cart is identified by the user ID.

- Product info (e.g., name, price) is retrieved via the **Catalog Service**. c
