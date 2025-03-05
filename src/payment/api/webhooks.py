import stripe
from django.conf import settings
from ninja.errors import HttpError
from ninja.router import Router

from common.utils.http_client import make_request

from .repository import PaymentRepository

router = Router()


@router.post("webhook/")
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpError(400, "Invalid payload")
    except stripe.SignatureVerificationError:
        return HttpError(400, "Invalid signature")

    if event.type == 'checkout.session.completed':
        session = event['data']['object']
        if session.mode == 'payment' and session.payment_status == 'paid':
            data = {
                "paid": True,
            }

            make_request(
                method="PATCH",
                payload=data,
                url=settings.ORDER_API_URL + '/' + session.client_reference_id,
            )

            instance = PaymentRepository.get(order_id=session.client_reference_id)
            PaymentRepository.update(
                instance, transaction_id=session.payment_intent, status="paid"
            )

    return {"status": "success"}
