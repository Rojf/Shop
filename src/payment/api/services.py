import time
from decimal import Decimal
from typing import Dict, Optional

import stripe
from django.conf import settings
from ninja import Schema
from ninja.errors import HttpError
from stripe import StripeError

from common.utils.generate import generate_unique_id

from .repository import PaymentRepository

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


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


def build_stripe_session_data(order: Dict) -> Dict:
    """Generates data for the Stripe payment session."""

    success_url = 'http://example.com/completed/'
    cancel_url = 'http://example.com/canceled/'

    session_data = {
        'mode': 'payment',
        'client_reference_id': order.get('order_id', 0),
        'success_url': success_url,
        'cancel_url': cancel_url,
        'expires_at': int(time.time() + (60 * 30)),
        'line_items': [],
    }

    for item in order.get('items', []):
        session_data['line_items'].append(format_stripe_line_item(item))

    return session_data


def create_stripe_checkout_session(
    session_data: dict,
) -> stripe.checkout.Session:
    """Creates and returns Stripe Checkout Session."""

    try:
        session = stripe.checkout.Session.create(**session_data)

        if session is None:
            raise HttpError(500, "")

        return session
    except StripeError as e:
        raise HttpError(500, f"Stripe error: {str(e)}") from e


def cancel_an_existing_stripe_session(existing_session_id: Optional[str]):
    if existing_session_id:
        try:
            stripe.checkout.Session.expire(existing_session_id)
        except StripeError:
            pass


def get_payment_update_params(
    order: dict, payment_data: Schema, stripe_session_id: str
) -> dict:
    return {
        'order_id': order.get('order_id'),
        'defaults': {'amount': order.get('amount', 0.00), **payment_data.dict()},
        'create_defaults': {
            'payment_id': generate_unique_id(),
            'user_id': generate_unique_id(),
            'amount': order.get('amount', 0.00),
            'currency': order.get('currency', 'USD'),
            'status': 'pending',
            'transaction_id': stripe_session_id,
            **payment_data.dict(),
        },
    }


def payment_process_service(transaction_id: str, order: dict, payment_data: Schema):
    cancel_an_existing_stripe_session(existing_session_id=transaction_id)

    checking_order_availability_in_session(order)
    stripe_session = create_stripe_checkout_session(build_stripe_session_data(order))

    PaymentRepository.update_or_create(
        **get_payment_update_params(order, payment_data, stripe_session.id)
    )

    return stripe_session


def checking_order_availability_in_session(order_session):
    if order_session is None:
        raise ValueError(
            """
            Order not found in session.
            To avoid making an exception.
            The user needs to add the product to the cart and create an order.
            """
        )
