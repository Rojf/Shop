from utils.base_repository import BaseRepository

from .models import Payment, Refund


class PaymentRepository(BaseRepository):
    model = Payment


class RefundRepository(BaseRepository):
    model = Refund
