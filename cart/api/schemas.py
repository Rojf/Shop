from ninja import Schema
from typing import Optional, List, Dict
from datetime import datetime


class CategoriesSchema(Schema):
    name: str
    slug: str


class ProductsSchema(Schema):
    id: int
    name: str
    description: str
    price: float
    #currency: str
    available: bool
    category: CategoriesSchema
    # color: Optional[str]
    # size: Optional[str]
    image: Optional[str]
    created: datetime
    updated: datetime


class CartProductsSchema(Schema):
    id: int
    name: str
    price: float
    # currency: str
    color: Optional[str]
    size: Optional[str]
    image_url: Optional[str]
    
class CartItemSchema(Schema):
    product: CartProductsSchema
    quantity: int
    total_price: float


class CartSchema(Schema):
    items: Optional[Dict[str, CartItemSchema]] = {}
    total_quantity: int
    total_price: float


class RequestDataSchema(Schema):
    product_id: int
    quantity: int
    override: bool

