# 💳 Payment Service

The Payment Service processes transactions, handles payment intents, and verifies completed payments using external providers like **Stripe**.


---

## 🔌 API Endpoints

### POST `/api/v1/payment/process/`

Creates a payment session for a given order.

**Request Body:**

```json
{
  "payment_method": "card",
  "payment_gateway": "stripe"
}
```

**Response:**

```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_abc123"
}
```


---

### POST `/api/v1/payment/webhook/`

Stripe sends payment status updates to this endpoint.

**Note:** You should configure this webhook URL in your Stripe dashboard.

**Stripe Payload Example:**

```json
{
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_test_abc123",
      "payment_status": "paid",
      "metadata": {
        "order_id": 123
      }
    }
  }
}
```


---

## 💰 Payment Flow

1. **The user collects the cart** through the `Cart Service`.

2. When the user clicks the "Checkout" button on the frontend, **order data is sent to the `Order Service`**.

3. The `Order Service` saves the order (e.g., with the status "waiting for payment"), but does not handle the payment process itself.

4. At the moment when the user clicks the "Proceed to Payment" button, **the frontend sends a request directly to the `Payment Service`** to create a session.

5. The `Payment Service` creates the payment session and returns the **URL for the payment page**.

6. The user is redirected to the **Stripe page** to complete the payment.

This simplifies the process, as the `Order Service` is responsible only for creating and managing the order, while payment is handled by the `Payment Service`, with direct interaction between the frontend and the payment service.


---

## ⚙️ Environment Variables

| Variable                       | Description            |
| ------------------------------ | ---------------------- |
| `STRIPE_SECRET_KEY`            | Stripe secret key      |
| `STRIPE_WEBHOOK_SECRET`        | Webhook signing secret |
| `STRIPE_PUBLISHABLE_KEY`       |                        |
| `ALLOWED_HOSTS`                |                        |
| `DEBUG`                        |                        |
| `ORDER_API_URL`                |                        |
| `SECRET_KEY`<br>               |                        |
| `CELERY_BROKER_URL`            |                        |
| `CELERY_RESULT_BACKEND`        |                        |
| `CELERY_TASK_DEFAULT_QUEUE`    |                        |
| `CELERY_TASK_DEFAULT_EXCHANGE` |                        |
| `SUCCESS_URL`                  |                        |
| `CANCEL_URL`                   |                        |

PYTHONUNBUFFERED=1


---

## 🧪 Testing

```bash
pytest -v src/payment/tests/
```



---

## 🛠️ Notes

- All monetary operations are handled in **Stripe**.

- Internal validation ensures the user cannot modify `amount` or `order_id`.

- Webhooks must be verified using Stripe’s signing secret.
