import os
from datetime import datetime

import django
from celery import Celery
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

app = Celery(
    "notifications_service",
)
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task(name="send_payment_notification")
def send_payment_notification(**kwargs):
    subject = "Payment confirmation."
    payment_date = datetime.fromtimestamp(kwargs['payment_date'])

    html_content = render_to_string(
        'emails/payment_confirmation_email.html',
        {
            'amount_subtotal': kwargs['amount_subtotal'],
            'amount_total': kwargs['amount_total'],
            'payment_date': payment_date,
            'user_name': kwargs['order']['user_details']['first_name'].capitalize(),
            'order_id': kwargs['order']['order_id'],
            'products': kwargs['order']['items'],
            'tax': kwargs['order']['inclubing_taxes'],
            'shipping_method': kwargs['order']['delivery_details']['delivery_type'],
            'shipping_cost': kwargs['order']['shipping_cost'],
        },
    )

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [kwargs['order']['user_details']['email']],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
