from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.db import DatabaseError, transaction, IntegrityError
from django.conf import settings
from django.core.cache import cache
from ninja.router import Router
from ninja.errors import HttpError
from ninja.pagination import paginate
import json

import weasyprint

from .schemas import OrderSchemaOut, CreateOrderSchemaIn, CreateOrderSchemaOut, StatusUpdateSchemaIn, ErrorSchemaOut
from utils.requests import make_request_with_session_cookie
from utils.generate import generate_unique_id
from .Repository import OrdersRepository, OrderItemRepository, UserRepository, DeliveryRepository
# from .tasks import order_creared as celery_order_created


router = Router()


@router.get('', response=list[OrderSchemaOut])
@paginate
def view_orders(request):
    try:
        if not request.user.is_authenticated:
            raise HttpError(401, 'Unauthorized')

        orders = OrdersRepository.filter(
            user_details__user_id=request.user.id,
            available=True,
            prefetch_related=['user_details', 'delivery_details', 'items']
        )

        return orders
    except DatabaseError:
        # logger.error(f"Database error occurred: {str(e)}")
        raise HttpError(500, 'Internal Server Error')
    except HttpError as e:
        raise e
    except Exception as e:
        # logging.error(f'{e}')
        raise HttpError(500, 'The server couldn\'t do what you asked.')


@router.get('{order_id}/', response={200: OrderSchemaOut, 404: ErrorSchemaOut})
def view_order(request, order_id: int):
    order_instance = get_order(
        order_id,
        available=True, 
        prefetch_related=['user_details', 'delivery_details', 'items']
    )

    return 200, order_instance


@router.post('', response={201: CreateOrderSchemaOut, 400: dict})
def create_order(request, data: CreateOrderSchemaIn):
    cart = make_request_with_session_cookie(request=request, url=settings.CART_API_URL+'cart/')

    match cart:
        case None:
            return 400, {"detail": "Cart data is not available"}
        case {"items": items} if not items:
            return 400, {"detail": "Bad request, no items in cart"}

    order_instance = OrdersRepository.model(
        order_id=generate_unique_id(),
        cart_id=generate_unique_id(),
        status='pending',
        currency='USD',
        shipping_cost=0,       # We need to write a function to count.
        inclubing_taxes=0      # We need to write a function to count.
    )

    user_instance = UserRepository.model(
        order=order_instance,
        user_id=generate_unique_id(), # If it is created by an anonymous user, specify the ID of the anonymous user.
        first_name=data.first_nema,
        last_name=data.last_name,
        email=data.email,
        phone_number=data.phone_number
    )

    delivery_instance = DeliveryRepository.model(
        order=order_instance,
        delivery_type=data.delivery_type,
        comment_to_delivery=data.comment_to_delivery,
        address_1=data.address_1,
        address_2=data.address_1,
        postal_code=data.postal_code,
        city=data.city,
        country=data.country
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
            quantity=item['quantity']
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

        data_cache = {
            session_cookie: {
                'order_id': order_instance.order_id
            }
        }

        cache.set(settings.SESSION_COOKIE_NAME, json.dumps(data_cache), timeout=1_250_000)
        # return redirect(reverse('payment:process'))

        return 201, {'detail': 'The order is placed.'}

    except IntegrityError as e:
        return 400, {"detail": "Failed to create order. Transaction rolled back.", "error": str(e)}
    except Exception as e:
        return 400, {"detail": "An unexpected error occurred.", "error": str(e)}
    

def get_order(order_id: int, **kwargs):
    try:
        instance = OrdersRepository.get(order_id=order_id, **kwargs)
        if not instance:
            # logging.error('Order does not exist.')
            raise HttpError(404, 'Order does not exist.')
    except HttpError as e:
        raise e
    except Exception as e:
        # logging.error(f'The order status could not be displayed. Error: {e}')
        raise HttpError(500, 'The server couldn\'t do what you asked.')
    
    return instance


def update_status(order_instance, status: str):
    try:
        OrdersRepository.update(order_instance, status=status)
        if order_instance.status != status:
            # logging.error('Failed to update the status.')
            raise HttpError(400, 'Failed to update the status.')
    except HttpError as e:
        raise e
    except Exception as e:
        # logging.error(f'{e}')
        raise HttpError(500, 'The server couldn\'t do what you asked.')
    
    return f'The order has been {status}.'


@router.post('{order_id}/cancel/', response={200: dict, 500: dict})
def cancel_order(request, order_id: int):
    obj = get_order(int(order_id), available=True)
    if request.user.is_staff and obj.status is not ['pending', 'processing'] or obj.status != 'pending':
        raise HttpError(400, 'The order can\'t be cancelled.')

    response_data = update_status(obj, 'cancelled')

    return 200, {'detail': response_data}


@router.patch('{order_id}/', response={200: dict, 500: dict})
def update_order(request,  order_id: int, data: StatusUpdateSchemaIn):
    obj = get_order(int(order_id), available=True)
    response_data = update_status(obj, str(data.status.value))

    # cart.clear()
    # celery_order_created.delay(order.id)

    return 200, {'detail': response_data}


@router.post('{order_id}/refund/')
def refund_order(request, order_id: int):
    pass


@staff_member_required
def admin_order_pdf(request, order_id):
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

