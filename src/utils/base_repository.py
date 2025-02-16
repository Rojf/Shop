from typing import Generic, Optional, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, QuerySet

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T]):
    model: type[T]

    @classmethod
    def get(cls, *args, **kwargs) -> Optional[T]:
        try:
            select_related = kwargs.pop('select_related', [])
            prefetch_related = kwargs.pop('prefetch_related', [])
            return (
                cls.model.objects.select_related(*select_related)
                .prefetch_related(*prefetch_related)
                .get(*args, **kwargs)
            )
        except ObjectDoesNotExist:
            return None

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

        return (
            cls.model.objects.select_related(*select_related)
            .prefetch_related(*prefetch_related)
            .filter(*args, **kwargs)
        )

    @classmethod
    def create(cls, *args, **kwargs) -> tuple[T, bool]:
        return cls.model.objects.get_or_create(*args, **kwargs)

    @classmethod
    def update(cls, instance, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, instance) -> None:
        instance.delete()
