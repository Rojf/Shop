from decimal import Decimal
from typing import Dict, Optional

from ninja import Schema


class CartProductsSchema(Schema):
    id: int
    name: str
    price: Decimal
    # currency: str
    color: Optional[str]
    size: Optional[str]
    image_url: Optional[str]


class CartItemSchema(Schema):
    product: CartProductsSchema
    quantity: int
    total_price: Decimal


class CartSchema(Schema):
    items: Optional[Dict[str, CartItemSchema]] = {}
    total_quantity: int
    total_price: Decimal


class RequestDataSchema(Schema):
    product_id: int
    quantity: int
    override: bool
