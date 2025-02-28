from typing import Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.models import Model, QuerySet
from ninja.errors import HttpError

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T]):
    model: type[T]

    @classmethod
    def get(cls, *args, **kwargs) -> T:
        select_related = kwargs.pop('select_related', [])
        prefetch_related = kwargs.pop('prefetch_related', [])

        try:
            return (
                cls.model.objects.select_related(*select_related)
                .prefetch_related(*prefetch_related)
                .get(*args, **kwargs)
            )
        except ObjectDoesNotExist as exc:
            raise HttpError(404, f'{cls.model.__name__} does not exist.') from exc

    @classmethod
    def all(cls, *args, **kwargs) -> QuerySet[T]:
        select_related = kwargs.pop('select_related', [])
        prefetch_related = kwargs.pop('prefetch_related', [])

        return (
            cls.model.objects.select_related(*select_related)
            .prefetch_related(*prefetch_related)
            .all(*args, **kwargs)
        )

    @classmethod
    def filter(cls, *args, **kwargs) -> QuerySet[T]:
        select_related = kwargs.pop('select_related', [])
        prefetch_related = kwargs.pop('prefetch_related', [])

        try:
            return (
                cls.model.objects.select_related(*select_related)
                .prefetch_related(*prefetch_related)
                .filter(*args, **kwargs)
            )

        except ObjectDoesNotExist as exc:
            raise HttpError(404, f'{cls.model.__name__} does not exist.') from exc
        except DatabaseError as exc:
            # logger.error(f"Database error occurred: {str(e)}")
            raise HttpError(500, 'Internal Server Error') from exc

    @classmethod
    def create(cls, *args, **kwargs) -> tuple[T, bool]:
        return cls.model.objects.get_or_create(*args, **kwargs)

    @classmethod
    def update(cls, instance, **kwargs) -> T:
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, instance) -> None:
        instance.delete()
