from datetime import datetime
from enum import Enum
from typing import List, Optional

from ninja import Field, Schema
from ninja.errors import ValidationError


class BaseDelivery(Schema):
    delivery_type: str
    comment_to_delivery: Optional[str]
    address_1: str
    address_2: str
    postal_code: int
    city: str
    country: str


class DeliveryDetails(BaseDelivery):
    tracking_id: Optional[str]
    tracking_url: Optional[str]
    delivery_date: Optional[datetime] = None


class UserDetails(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: str


class ItemDetails(Schema):
    name: str
    product_id: int
    image_url: str
    size: str
    color: str
    price: float
    quantity: int


class OrderSchemaOut(Schema):
    order_id: str = Field(
        ...,
        description="order_id (BigInt) passed as string to "
        "avoid precision loss in Swagger UI",
    )
    status: str
    currency: str
    amount: float
    shipping_cost: int
    inclubing_taxes: int
    created: datetime
    delivery_details: DeliveryDetails
    user_details: UserDetails
    items: List[ItemDetails]

    @staticmethod
    def resolve_order_id(obj):
        if not obj.order_id:
            return None
        return str(obj.order_id)


class CreateOrderSchemaIn(BaseDelivery, UserDetails):

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

    def __str__(self):
        return str(self.value)


class UpdateOrderSchemaIn(Schema):
    status: Optional[OrderStatusEnum]
    amount: Optional[float]
    paid: Optional[bool]
    user_details: Optional[UserDetails]
    delivery_details: Optional[BaseDelivery]
