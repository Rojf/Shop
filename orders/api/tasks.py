from celery import shared_task
from django.core.mail import send_mail

from .Repository import OrdersRepository


@shared_task
def order_creared(order_id):
    """
    The task of sending an email notification when an order is successfully created.

    :param order_id:
    :return:
    """

    order = OrdersRepository.get(
        order_id=order_id,
        prefetch_related=['user_details', 'delivery_details', 'items']
    )

    if not order:
        return 

    subject = f'Order nr. {order.order_id}'
    message = f'Dear {order.user_details.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.order_id}.'
    mail_sent = send_mail(subject, message, 'admin@shop.com', [order.email])

    return mail_sent
