from utils.repositories.base import BaseRepository
from .models import Order, OrderItem


class OrderItemRepository(BaseRepository):
    model = OrderItem


class OrderRepository(BaseRepository):
    model = Order
