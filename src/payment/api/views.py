from ninja import Router

from services.order_service import fetch_order_details
from services.payment_service import (
    build_stripe_session_data,
    create_stripe_checkout_session,
)
from utils.generate import generate_unique_id
from utils.sessions_utils import get_session_from_redis

from .repository import PaymentRepository
from .schemas import PaymentCreateSchema

router = Router()


@router.post('process/')
def payment_process(request, payment_data: PaymentCreateSchema):
    redis_session_data = get_session_from_redis(request)

    order_id = redis_session_data.get('order_id', '')
    order = fetch_order_details(order_id)

    session_data = build_stripe_session_data(order)

    PaymentRepository.create(
        payment_id=generate_unique_id(),
        order_id=order_id,
        user_id=generate_unique_id(),
        amount=order.get('amount', 0.00),
        currency=order.get('currency', 'usd'),
        status="pending",
        transaction_id=None,
        **payment_data.dict()
    )

    return {"payment_url": create_stripe_checkout_session(session_data)}
