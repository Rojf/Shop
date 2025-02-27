import time
from decimal import Decimal
from typing import Dict, Optional

import stripe
from django.conf import settings
from ninja.errors import HttpError
from stripe import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def build_stripe_session_data(order: Dict) -> Dict:
    """Generates data for the Stripe payment session."""

    success_url = 'http://example.com/completed/'
    cancel_url = 'http://example.com/canceled/'

    session_data = {
        'mode': 'payment',
        'client_reference_id': order.get('order_id'),
        'success_url': success_url,
        'cancel_url': cancel_url,
        'expires_at': int(time.time() + (60 * 30)),
        'line_items': [],
    }

    for item in order.get('items', []):
        session_data['line_items'].append(format_stripe_line_item(item))

    return session_data


def format_stripe_line_item(item):
    """Formats the product data for Stripe Checkout."""

    return {
        'price_data': {
            'unit_amount': int(Decimal(str(item.get('price', 0))) * Decimal('100')),
            'currency': 'usd',
            'product_data': {
                'name': item.get('name', 'Unknown Product'),
                'images': (
                    [item.get('image_url')]
                    if item.get('image_url')
                    else [
                        (
                            'https://us.sunspel.com/cdn/shop/'
                            'files/mtsh0181-bkaa-1.jpg?v=1720096619'
                        )
                    ]
                ),
            },
        },
        'quantity': item.get('quantity', 1),
    }


def create_stripe_checkout_session(session_data: dict) -> Optional[str]:
    """Creates and returns Stripe Checkout Session."""

    try:
        session = stripe.checkout.Session.create(**session_data)

        if session is None:
            raise HttpError(500, "")

        return session.url
    except StripeError as e:
        raise HttpError(500, f"Stripe error: {str(e)}") from e
