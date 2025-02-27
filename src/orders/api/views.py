import json

import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja.router import Router

from utils.generate import generate_unique_id
from utils.http_client import make_request_with_session_cookie
from utils.sessions_utils import get_session_from_redis

from .repository import (
    DeliveryRepository,
    OrderItemRepository,
    OrdersRepository,
    UserRepository,
)
from .schemas import (
    CreateOrderSchemaIn,
    OrderSchemaOut,
    UpdateOrderSchemaIn,
)

# from .tasks import order_creared as celery_order_created


router = Router()


@router.get('', response=list[OrderSchemaOut])
@paginate
def view_orders(request):
    _ = request
    # if not request.user.is_authenticated:
    #     raise HttpError(401, 'Unauthorized')

    orders = OrdersRepository.filter(
        #    user_details__user_id=request.user.id,
        available=True,
        prefetch_related=['user_details', 'delivery_details', 'items'],
    )

    return orders


@router.get('{order_id}/', response={200: OrderSchemaOut, 404: dict})
def view_order(request, order_id: int):
    _ = request
    order_instance = OrdersRepository.get(
        order_id=order_id,
        available=True,
        prefetch_related=['user_details', 'delivery_details', 'items'],
    )

    return 200, order_instance


@router.post('', response={201: dict, 400: dict, 409: dict})
def create_order(request, data: CreateOrderSchemaIn):
    cart = make_request_with_session_cookie(request=request, url=settings.CART_API_URL)

    match cart:
        case None:
            return 400, {"detail": "Cart data is not available"}
        case {"items": items} if not items:
            return 400, {"detail": "Bad request, no items in cart"}

    order_id = get_session_from_redis(request).get('order_id', None)

    if order_id and isinstance(order_id, int):
        return 409, {"detail": "The order has already been created."}

    order_instance = OrdersRepository.model(
        order_id=generate_unique_id(),
        # REDUNDANT I need to delete the Cart_id column from the database.
        cart_id=generate_unique_id(),
        status='pending',
        amount=cart['total_price'],
        paid=False,
        currency='USD',
        shipping_cost=0,  # We need to write a function to count.
        inclubing_taxes=0,  # We need to write a function to count.
    )

    user_instance = UserRepository.model(
        order=order_instance,
        # If it is created by an anonymous user, specify the ID of the anonymous user.
        user_id=generate_unique_id(),
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone_number=data.phone_number,
    )

    delivery_instance = DeliveryRepository.model(
        order=order_instance,
        delivery_type=data.delivery_type,
        comment_to_delivery=data.comment_to_delivery,
        address_1=data.address_1,
        address_2=data.address_1,
        postal_code=data.postal_code,
        city=data.city,
        country=data.country,
    )

    order_items = [
        OrderItemRepository.model(
            order=order_instance,
            product_id=item['product']['id'],
            name=item['product']['name'],
            image_url=item['product']['image_url'],
            size=item['product']['size'],
            color=item['product']['color'],
            price=item['product']['price'],
            quantity=item['quantity'],
        )
        for item in cart["items"].values()
    ]

    try:
        with transaction.atomic():
            order_instance.save()
            user_instance.save()
            delivery_instance.save()
            OrderItemRepository.bulk_create(order_items)

        session_cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

        add_order_id_to_cache = {'order_id': order_instance.order_id}

        session_data = get_session_from_redis(request)

        session_data.update(add_order_id_to_cache)

        cache.set(session_cookie, json.dumps(session_data), timeout=1_250_000)
        # return redirect(reverse('payment:process'))

        return 201, {'detail': 'The order is placed.'}

    except IntegrityError as exc:
        return 400, {
            "detail": "Failed to create order. Transaction rolled back.",
            "error": str(exc),
        }


@router.post('{order_id}/cancel/', response={200: dict, 500: dict})
def cancel_order(request, order_id: int):
    order_instance = OrdersRepository.get(
        order_id=int(order_id),
        available=True,
    )

    if (
        request.user.is_staff
        and order_instance.status not in ['pending', 'processing']
        or order_instance.status != 'pending'
    ):
        raise HttpError(400, 'The order can\'t be cancelled.')

    OrdersRepository.update(order_instance, status='cancelled')

    return 200, {'detail': 'The order has been cancelled.'}


@router.patch('{order_id}/', response={200: dict, 500: dict})
def update_order(request, order_id: int, data: UpdateOrderSchemaIn):
    _ = request

    order_instance = OrdersRepository.get(
        order_id=int(order_id),
        available=True,
        select_related=['user_details', 'delivery_details'],
    )

    order_data = {"status": data.status, "amount": data.amount, "paid": data.paid}
    user_data = data.user_details.dict() if data.user_details else {}
    delivery_data = data.delivery_details.dict() if data.delivery_details else {}

    try:
        with transaction.atomic():
            OrdersRepository.update(order_instance, **order_data)
            UserRepository.update(order_instance.user_details, **user_data)
            DeliveryRepository.update(order_instance.delivery_details, **delivery_data)

        return 200, {'detail': 'The order has been updated.'}
    except HttpError as e:
        raise e
    except Exception as e:
        raise HttpError(500, f'Failed to update order: {str(e)}') from e


@router.post('{order_id}/refund/')
def refund_order(request, order_id: int):
    _ = request
    _ = order_id
    return ''


@staff_member_required
def admin_order_pdf(request, order_id):
    _ = request
    order = get_object_or_404(OrdersRepository.model, order_id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{getattr(order, 'order_id')}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))]
    )

    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(OrdersRepository.model, order_id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
