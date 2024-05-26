from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.Repository import ProductRepository
from .cart import Cart
from .forms import CartAddProductFrom


def cart_detail(request):
    cart = Cart(request)

    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    print(id(cart))
    product = get_object_or_404(ProductRepository.model, id=product_id)
    form = CartAddProductFrom(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductRepository.model, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')
