from ninja import Router

from services.payment_service import (
    build_stripe_session_data,
    cancel_an_existing_stripe_session,
    create_stripe_checkout_session,
)
from utils.generate import generate_unique_id

from .repository import PaymentRepository
from .schemas import PaymentCreateSchema

router = Router()


@router.post('process/')
def payment_process(request, payment_data: PaymentCreateSchema):
    session = request.session
    order = session.get('order')
    order_id = order.get('order_id')
    session_data = build_stripe_session_data(order)

    cancel_an_existing_stripe_session(existing_session_id=session.get('transaction_id'))
    stripe_session = create_stripe_checkout_session(session_data)

    defaults = {'amount': order.get('amount', 0.00), **payment_data.dict()}
    create_defaults = {
        'payment_id': generate_unique_id(),
        'user_id': generate_unique_id(),
        'amount': order.get('amount', 0.00),
        'currency': order.get('currency', 'USD'),
        'status': 'pending',
        'transaction_id': stripe_session.id,
        **payment_data.dict(),
    }

    PaymentRepository.update_or_create(
        order_id=order_id, defaults=defaults, create_defaults=create_defaults
    )

    return {"payment_url": stripe_session.url}
