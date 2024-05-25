from django.contrib.auth.models import User

from .base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def create_user(cls, *args, **kwargs):
        return cls.model.objects.create_user(*args, **kwargs)
