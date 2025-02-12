from utils.base_repository import BaseRepository

from .models import Category, Product


class CategoryRepository(BaseRepository):
    model = Category


class ProductRepository(BaseRepository):
    model = Product
