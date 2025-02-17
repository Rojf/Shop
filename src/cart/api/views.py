from ninja import Router

from utils.requests import make_request

from .cart import Cart
from .schemas import CartSchema, RequestDataSchema

router = Router()


@router.get("", url_name="cart_detail", response=CartSchema)
def view_cart(request):
    cart = Cart(request)

    return cart.to_dict()


@router.post("items/", response=CartSchema)
def add_to_cart(request, data: RequestDataSchema):
    cart = Cart(request)

    product_id = data.product_id

    _, product = make_request(
        method="GET", url=f"http://127.0.0.1:8001/api/v1/catalog/{product_id}/"
    )

    cart.add(product=product, quantity=data.quantity, override_quantity=data.override)

    # return JsonResponse({"detail": "Product added to cart", "cart": cart.to_dict()})
    return cart.to_dict()


@router.delete("items/{int:product_id}/", response=CartSchema)
def remove_from_cart(request, product_id: int):
    cart = Cart(request)

    cart.remove(product_id)

    # return JsonResponse({"detail": "Product removed from cart", "cart": cart.to_dict()})
    return cart.to_dict()
