from datetime import datetime
from enum import Enum
from typing import List, Optional

from ninja import Schema
from ninja.errors import ValidationError


class DeliveryDetailsOut(Schema):
    tracking_id: Optional[str]
    tracking_url: Optional[str]
    delivery_date: Optional[datetime] = None
    delivery_type: str
    comment_to_delivery: Optional[str]
    address_1: str
    address_2: str
    postal_code: int
    city: str
    country: str


class UserDetails(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: str


class Item(Schema):
    name: str
    product_id: int
    image_url: str
    size: str
    color: str
    price: float
    quantity: int


class OrderTest(Schema):
    total_quintity: int
    total_price: int


class OrderSchemaOut(Schema):
    order_id: int
    status: str
    currency: str
    amount: float
    shipping_cost: int
    inclubing_taxes: int
    created: datetime
    delivery_details: DeliveryDetailsOut
    user_details: UserDetails
    items: List[Item]


class ErrorSchemaOut(Schema):
    detail: str


class CreateOrderSchemaIn(Schema):
    delivery_type: str
    address_1: str
    address_2: str
    city: str
    postal_code: int
    country: str
    comment_to_delivery: Optional[str]
    first_nema: str
    last_name: str
    phone_number: str
    email: str

    def validate_postal_code(self, value):
        if len(str(value)) != 5:
            raise ValidationError([{"detail": "Postal code must be 5 digits"}])
        return value


class OrderStatusEnum(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class CreateOrderSchemaOut(Schema):
    detail: str


class StatusUpdateSchemaIn(Schema):
    status: OrderStatusEnum
    paid: bool
