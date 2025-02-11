from utils.repositories.base import BaseRepository
from .models import Category, Product


class CategoryRepository(BaseRepository):
    model = Category


class ProductRepository(BaseRepository):
    model = Product
