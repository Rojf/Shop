from django.conf import settings
from django.core.cache import cache
from ninja import Router
from ninja.errors import HttpError
import json

from decimal import Decimal
import stripe

from utils.requests import make_request


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


router = Router()


@router.post('process/')
def payment_process(request):
    session_cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    redis_sessions = cache.get(settings.SESSION_COOKIE_NAME)
    load_session = json.loads(redis_sessions).get(session_cookie)

    order_id = load_session.get('order_id')
    status, order = make_request(
        url=settings.ORDER_API_URL+f'orders/{order_id}/',
        method='GET'
    )

    if status != 200:
        raise HttpError(status, '')

    success_url = 'http://example.com/completed/'
    cancel_url = 'http://example.com/canceled/'

    session_data = {
        'mode': 'payment',
        'client_reference_id': order.get('order_id'),
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': []
    }

    for item in order.get('items', []):
        print("image", item.get('image_url', ''))
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': int(Decimal(str(item.get('price'))) * Decimal('100')),
                'currency': 'usd',
                'product_data': {
                    'name': item.get('name'),
                    'images': [item.get('image_url')] \
                        if item.get('image_url') \
                        else ['https://us.sunspel.com/cdn/shop/files/mtsh0181-bkaa-1.jpg?v=1720096619']
                },
            },
            'quantity': item.get('quantity'),
        })
        
    session = stripe.checkout.Session.create(**session_data)

    return session.url      # redirect 303

