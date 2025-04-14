
# 📦 Catalog Service

The Catalog Service manages products, categories, availability, and search functionality.

---

## 🔌 API Endpoints

### GET `/api/v1/catalog/products/`

Returns a list of all products.

**Response:**

```json
[
  {
    "id": 101,
    "name": "Wireless Mouse",
    "description": "Ergonomic design with 2.4GHz connection",
    "price": 25.99,
    "in_stock": true,
    "category_id": 3
  },
  ...
]
```


---

### GET `/api/v1/catalog/products/{id}`

Returns details for a specific product.

**Response:**

```json
{
  "id": 101,
  "name": "Wireless Mouse",
  "description": "Ergonomic design with 2.4GHz connection",
  "price": 25.99,
  "in_stock": true,
  "category": {
    "id": 3,
    "name": "Accessories"
  }
}
```


---

### POST `/api/v1/catalog/products/`

> Admin only
> Creates a new product.

**Request Body:**

```json
{
  "name": "Bluetooth Speaker",
  "description": "Portable speaker with deep bass",
  "price": 45.00,
  "category_id": 4,
  "in_stock": true
}
```

**Response**

```json
{
  "id": 102,
  "message": "Product created"
}
```


---

### GET `/api/v1/catalog/categories/`

Returns a list of product categories.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Laptops"
  },
  {
    "id": 2,
    "name": "Smartphones"
  }
]
```


---

## 🔍 Search Example

Search products by name:

```bash
GET /api/v1/catalog/products/?search=mouse
```


---

## ⚙️ Environment Variables

| Variable              | Description                   |
| --------------------- | ----------------------------- |
| `CATALOG_DB_HOST`     | Host for the product database |
| `CATALOG_DB_NAME`     | PostgreSQL database name      |
| `CATALOG_DB_USER`     | Database username             |
| `CATALOG_DB_PASSWORD` | Database password             |

---

## 🧪 Testing

Run tests for the catalog service:

```bash
pytest -v src/catalog/tests/
```


---

## 🛠️ Notes

- The product data is stored in **PostgreSQL**.

- Admin endpoints require authentication and role verification.

- Cart and Order services depend on product availability from this service.
