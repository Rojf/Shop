from django.conf import settings
from ninja.errors import HttpError

from utils.http_client import make_request


def fetch_order_details(order_id: int) -> dict:
    """Requests the order details by its ID."""

    if not order_id:
        raise HttpError(400, "Order ID is required")

    url = f"{settings.ORDER_API_URL}/{order_id}/"
    order = make_request(url=url, method="GET")

    if not order:
        raise HttpError(404, "Order not found")

    return order
