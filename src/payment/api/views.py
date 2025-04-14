from ninja import Router

from .schemas import PaymentCreateSchema
from .services import payment_process_service

router = Router()


@router.post('process/')
def payment_process(request, payment_data: PaymentCreateSchema):
    payment_session = request.session.get('payment', {})
    order_session = request.session.get('order')

    stripe_session = payment_process_service(
        transaction_id=payment_session.get('transaction_id', 0),
        order=order_session,
        payment_data=payment_data,
    )

    request.session.update({'payment': {'transaction_id': stripe_session.id}})

    return {"checkout_url": stripe_session.url}
