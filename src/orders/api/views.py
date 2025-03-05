import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from ninja.pagination import paginate
from ninja.router import Router

from .repository import (
    OrdersRepository,
)
from .schemas import (
    CreateOrderSchemaIn,
    OrderSchemaOut,
    UpdateOrderSchemaIn,
    UpdateOrderStatusSchemaIn,
)
from .services import (
    cancel_order_service,
    create_order_service,
    get_order_service,
    order_list_service,
    update_order_service,
    update_order_status_service,
)

# from .tasks import order_creared as celery_order_created


router = Router()


@router.get('', response=list[OrderSchemaOut])
@paginate
def view_orders(request):
    user_is_authenticated = request.user.is_authenticated

    orders = order_list_service(user_is_authenticated)

    return orders


@router.get('{order_id}/', response={200: OrderSchemaOut, 404: dict})
def view_order(request, order_id: int):
    _ = request

    order_instance = get_order_service(order_id)

    return 200, order_instance


@router.post('', response={201: dict})
def create_order(request, data: CreateOrderSchemaIn):
    session = request.session
    cart = session.get('cart')
    order_id = session.get('order', {}).get('order_id', None)

    order_instance = create_order_service(cart, order_id, data)

    session['order'] = OrderSchemaOut.from_orm(order_instance).dict()

    return 201, {'detail': 'The order is placed.'}


@router.post('{order_id}/cancel/', response={200: dict})
def cancel_order(request, order_id: int):
    user_is_staff = request.user.is_staff

    cancel_order_service(order_id, user_is_staff)

    return 200, {'detail': 'The order has been cancelled.'}


@router.patch('{order_id}/', response={200: dict})
def update_order(request, order_id: int, data: UpdateOrderSchemaIn):
    session = request.session
    cart = session.get('cart')

    update_order_service(cart, order_id, data)

    return 200, {'detail': 'The order has been updated.'}


@router.post('{order_id}/refund/')
def refund_order(request, order_id: int):
    _ = request
    _ = order_id
    return 'Not implemented yet.'


@router.patch('{order_id}/update/')
def update_paid_and_status_order(request, order_id: int, data: UpdateOrderStatusSchemaIn):
    _ = request

    update_order_status_service(order_id, data)
    print(f"\n\nOrder_id - {order_id}\n\n")
    return 'Not implemented yet.'


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
