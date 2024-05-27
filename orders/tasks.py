from celery import shared_task
from django.core.mail import send_mail

from .Repository import OrderRepository


@shared_task
def order_creared(order_id):
    """
    The task of sending an email notification when an order is successfully created.

    :param order_id:
    :return:
    """

    order = OrderRepository.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@shop.com', [order.email])

    return mail_sent
