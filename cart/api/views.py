from ninja import Router

from .cart import Cart
from .requests import make_request
from .schemas import CartSchema, RequestDataSchema


router = Router()


@router.get("cart/", url_name="cart_detail", response=CartSchema)
def view_cart(request):
    cart = Cart(request)
    
    return cart.to_dict()


@router.post("cart/items/", response=CartSchema)
def add_to_cart(request, data: RequestDataSchema):
    cart = Cart(request)

    product_id = data.product_id
    
    # Нужно создать функцию которая будет оброщаться к Microserves Shop по API вместо get_db
    _, product = make_request(method="GET", url=f"http://127.0.0.1:8001/api/v1/catalog/{product_id}/")

    cart.add(product=product, quantity=data.quantity, override_quantity=data.override)

    #return JsonResponse({"detail": "Product added to cart", "cart": cart.to_dict()})
    return cart.to_dict()


@router.delete("cart/items/{int:product_id}/", response=CartSchema)
def remove_from_cart(request, product_id: int):
    cart = Cart(request)
    
    # Нужно создать функцию которая будет оброщаться к Microserves Shop по API вместо get_db
    cart.remove(product_id)

    #return JsonResponse({"detail": "Product removed from cart", "cart": cart.to_dict()})
    return cart.to_dict()

