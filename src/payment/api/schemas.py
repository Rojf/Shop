from enum import Enum

from ninja import Schema


class CurrencyEnum(Enum):
    USD = "usd"
    EUR = "eur"


class PaymentStatusEnum(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethodEnum(Enum):
    CARD = "card"
    PAYPAL = "paypal"
    APPLE_PAY = "apple_pay"


class PaymentGatewayEnum(Enum):
    STRIPE = "stripe"


class PaymentOutSchema(Schema):
    payment_id: int
    order_id: int
    user_id: int
    amount: float
    currency: CurrencyEnum
    status: PaymentStatusEnum
    payment_method: PaymentMethodEnum


class PaymentCreateSchema(Schema):
    payment_method: PaymentMethodEnum = PaymentMethodEnum.CARD
    payment_gateway: PaymentGatewayEnum = PaymentGatewayEnum.STRIPE
