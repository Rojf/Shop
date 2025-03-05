from django.db import IntegrityError, transaction
from ninja.errors import HttpError

from common.utils.generate import generate_unique_id

from .repository import (
    DeliveryRepository,
    OrderItemRepository,
    OrdersRepository,
    UserRepository,
)


def order_list_service(user_is_authenticated: bool):
    if not user_is_authenticated:
        pass
        # raise HttpError(401, 'Unauthorized')

    orders = OrdersRepository.filter(
        #    user_details__user_id=request.user.id,
        available=True,
        prefetch_related=['user_details', 'delivery_details', 'items'],
    )

    return orders


def get_order_service(order_id):
    order_instance = OrdersRepository.get(
        order_id=order_id,
        available=True,
        prefetch_related=['user_details', 'delivery_details', 'items'],
    )

    return order_instance


def checking_cart(cart):
    match cart:
        case None:
            raise HttpError(400, "Cart data is not available")
        case {"items": items} if not items:
            raise HttpError(400, "Bad request, no items in cart")


def checking_order_for_existence(order_id: int):
    if OrdersRepository.filter(order_id=order_id, paid=False).exists():
        raise HttpError(
            409,
            "The order has already been created. If you need to update the order, "
            "need to make an update request. PATCH /v1/orders/{order_id}/",
        )


def create_order_service(cart, order_id, data):
    checking_cart(cart)
    checking_order_for_existence(order_id)

    order_instance = OrdersRepository.model(
        order_id=generate_unique_id(),
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

        order_instance = OrdersRepository.get(
            order_id=order_instance.order_id,
            available=True,
            prefetch_related=['user_details', 'delivery_details', 'items'],
        )

        return order_instance

    except IntegrityError as exc:
        raise HttpError(
            400, f"Failed to create order. Transaction rolled back. Reason: {str(exc)}"
        ) from exc


def cancel_order_service(order_id, user_is_staff):
    order_instance = OrdersRepository.get(
        order_id=int(order_id),
        available=True,
    )

    if (
        user_is_staff
        and order_instance.status not in ['pending', 'processing']
        or order_instance.status != 'pending'
    ):
        raise HttpError(400, 'The order can\'t be cancelled.')

    OrdersRepository.update(order_instance, status='cancelled')


def update_order_service(cart, order_id, data):
    checking_cart(cart)

    order_instance = OrdersRepository.get(
        order_id=int(order_id),
        available=True,
        prefetch_related=['user_details', 'delivery_details', 'items'],
    )

    order_data = {"status": data.status, "amount": cart.total_price, "paid": data.paid}
    user_data = data.user_details.dict() if data.user_details else {}
    delivery_data = data.delivery_details.dict() if data.delivery_details else {}

    try:
        with transaction.atomic():
            OrdersRepository.update(order_instance, **order_data)
            UserRepository.update(order_instance.user_details, **user_data)
            DeliveryRepository.update(order_instance.delivery_details, **delivery_data)

    except HttpError as e:
        raise e
    except Exception as e:
        raise HttpError(500, f'Failed to update order: {str(e)}') from e


def update_order_status_service(order_id, data):
    order_data = {"paid": data.paid}

    order = OrdersRepository.get(order_id=order_id)

    try:
        OrdersRepository.update(order, **order_data)

    except HttpError as e:
        raise e
    except Exception as e:
        raise HttpError(500, f'Failed to update order: {str(e)}') from e
