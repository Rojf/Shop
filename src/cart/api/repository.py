from django.conf import settings

from utils.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = settings.AUTH_USER_MODEL

    @classmethod
    def create_user(cls, *args, **kwargs):
        return cls.model.objects.create_user(*args, **kwargs)
