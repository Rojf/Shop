from django.shortcuts import render, get_object_or_404

from .Repository import CategoryRepository, ProductRepository
from cart.forms import CartAddProductFrom


def product_list(request, category_slug=None):
    category = None
    categories = CategoryRepository.all()
    products = ProductRepository.filter(available=True)

    if category_slug:
        # category = CategoryRepository.get(slug=category_slug)
        category = get_object_or_404(CategoryRepository.model, slug=category_slug)
        products = ProductRepository.filter(category=category)

    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories, 'products': products})


def product_detail(request, id, slug):
    # product = ProductRepository.get(id=id, slug=slug, available=True)
    product = get_object_or_404(ProductRepository.model, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductFrom

    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})
