from typing import Optional

from django.shortcuts import get_object_or_404
from ninja import Router

from .repository import CategoryRepository, ProductRepository
from .schemas import DataOutSchema, ProductsSchema

router = Router()


@router.get("", response=DataOutSchema)
def product_list(request, category_slug: Optional[str] = None):
    _ = request
    category = None
    category_slug = category_slug.lower() if category_slug else None
    categories = CategoryRepository.all()
    products = ProductRepository.filter(available=True)

    if category_slug:
        category = get_object_or_404(CategoryRepository.model, slug=category_slug)
        products = ProductRepository.filter(category=category)

    return {'category': category, 'categories': categories, 'products': products}


@router.get("{product_id}/", url_name="product_detail", response=ProductsSchema)
def product_detail(request, product_id: int):
    _ = request
    product = get_object_or_404(ProductRepository.model, id=product_id, available=True)

    return product
