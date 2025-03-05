from typing import Optional

from ninja import Router

from .schemas import DataOutSchema, ProductsSchema
from .services import get_product_service, product_list_service

router = Router()


@router.get("", response=DataOutSchema)
def product_list(request, category_slug: Optional[str] = None):
    _ = request
    category, categories, products = product_list_service(category_slug)

    return {'category': category, 'categories': categories, 'products': products}


@router.get("{product_id}/", url_name="product_detail", response=ProductsSchema)
def product_detail(request, product_id: int):
    _ = request

    return get_product_service(product_id)
