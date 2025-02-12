from utils.base_repository import BaseRepository

from .models import Delivery, Order, OrderItem, User


class OrderItemRepository(BaseRepository):
    model = OrderItem

    @classmethod
    def bulk_create(cls, items):
        return cls.model.objects.bulk_create(items)


class OrdersRepository(BaseRepository):
    model = Order


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def create_user(cls, *args, **kwargs):
        return cls.model.objects.create_user(*args, **kwargs)


class DeliveryRepository(BaseRepository):
    model = Delivery
