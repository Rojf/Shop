from utils.repositories.base import BaseRepository
from .models import Order, OrderItem, User, Delivery


class OrderItemRepository(BaseRepository):
    model = OrderItem

    @classmethod
    def bulk_create(cls, items):
        return cls.model.objects.bulk_create(items)


class OrdersRepository(BaseRepository):
    model = Order


class UserRepository(BaseRepository):
    model = User


class DeliveryRepository(BaseRepository):
    model = Delivery

