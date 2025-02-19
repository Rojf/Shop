from datetime import datetime
from typing import List, Optional

from ninja import Schema


class CategoriesSchema(Schema):
    name: str
    slug: str


class ProductsSchema(Schema):
    id: int
    category: CategoriesSchema
    name: str
    slug: str
    image_url: Optional[str]
    description: str
    price: float
    currency: str
    color: Optional[str]
    size: Optional[str]
    available: bool
    created: datetime
    updated: datetime


class DataOutSchema(Schema):
    category: Optional[CategoriesSchema]
    categories: List[CategoriesSchema]
    products: List[ProductsSchema]


class RequestDataSchema(Schema):
    category_slug: Optional[str] = None

    def resolve_lower_category_slug(self):
        return self.category_slug.lower() if self.category_slug else None
