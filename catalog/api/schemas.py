from ninja import Schema
from typing import Optional, List
from datetime import datetime


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
    category:   Optional[CategoriesSchema]
    categories: List[CategoriesSchema]
    products:   List[ProductsSchema]

