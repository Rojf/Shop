import stripe
from django.conf import settings
from ninja.errors import HttpError
from ninja.router import Router

from common.utils.http_client import make_request
from config.celery import app

from .repository import PaymentRepository

router = Router()


@router.post("")
def stripe_webhook(request):
    order_session = request.session.get('order')

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as exc:
        raise HttpError(400, f"Error parsing payload: {str(exc)}") from exc
    except stripe.SignatureVerificationError as exc:
        raise HttpError(400, f"Error parsing payload: {str(exc)}") from exc

    if event.type == 'checkout.session.completed':
        session = event['data']['object']
        if session.mode == 'payment' and session.payment_status == 'paid':
            data = {
                "paid": True,
            }

            make_request(
                method="PATCH",
                payload=data,
                url=settings.ORDER_API_URL
                + str(session.client_reference_id)
                + "/update/",
            )

            instance = PaymentRepository.get(order_id=session.client_reference_id)
            PaymentRepository.update(
                instance, transaction_id=session.payment_intent, status="paid"
            )

            app.send_task(
                "send_payment_notification",
                kwargs={
                    "order": order_session,
                    "payment_date": session.created,
                    "amount_subtotal": session.amount_subtotal,
                    "amount_total": session.amount_total,
                },
                queue="queue_notifications",
            )

    return {"status": "success"}
