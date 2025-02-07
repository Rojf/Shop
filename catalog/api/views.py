from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from .Repository import CategoryRepository, ProductRepository
from .schemas import DataOutSchema, ProductsSchema

api = NinjaAPI()


@api.get("catalog/", response=DataOutSchema)
def product_list(request, category_slug: str = None):
    category = None
    categories = CategoryRepository.all()
    products = ProductRepository.filter(available=True)

    if category_slug:
        category = get_object_or_404(CategoryRepository.model, slug=category_slug)
        products = ProductRepository.filter(category=category)

    return {'category': category, 'categories': categories, 'products': products}


@api.get("catalog/{int:id}/", url_name="product_detail", response=ProductsSchema)
def product_detail(request, id: int):
    product = get_object_or_404(ProductRepository.model, id=id, available=True)

    return product

