from django.conf import settings
from ninja import Router

from common.utils.http_client import make_request

from .schemas import CartSchema, RequestDataSchema
from .services import Cart

router = Router()


@router.get("", url_name="cart_detail", response=CartSchema)
def view_cart(request):
    cart = Cart(request)
    return cart.to_dict()


@router.post("items/", response=CartSchema)
def add_to_cart(request, data: RequestDataSchema):
    cart = Cart(request)

    product_id = data.product_id
    product = make_request(method="GET", url=f"{settings.CATALOG_API_URL}{product_id}/")

    cart.add(product=product, quantity=data.quantity, override_quantity=data.override)

    return cart.to_dict()


@router.delete("items/{int:product_id}/", response=CartSchema)
def remove_from_cart(request, product_id: int):
    cart = Cart(request)
    cart.remove(product_id)

    return cart.to_dict()


@router.delete("", response=CartSchema)
def clear_cart(request):
    cart = Cart(request)
    cart.clear()

    return cart.to_dict()
