from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

from orders.Repository import OrderRepository


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(sattus=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = OrderRepository.get(id=session.client_reference_id)
            except OrderRepository.model.DoesNotExist:
                return HttpResponse(status=404)

            order.paid = True
            order.save()

    return HttpResponse(status=200)

