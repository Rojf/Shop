from django.core.exceptions import ObjectDoesNotExist


class BaseRepository:
    model = None

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            select_related = kwargs.pop('select_related', [])
            prefetch_related = kwargs.pop('prefetch_related', [])
            return cls.model.objects.select_related(*select_related).prefetch_related(*prefetch_related).get(*args, **kwargs)
        except ObjectDoesNotExist:
            return

    @classmethod
    def all(cls, *args, **kwargs):
        select_related = kwargs.pop('select_related', [])
        prefetch_related = kwargs.pop('prefetch_related', [])
        return cls.model.objects.select_related(*select_related).prefetch_related(*prefetch_related).all(*args, **kwargs)

    @classmethod
    def created(cls, *args, **kwargs):
        return cls.model.objects.get_or_create(*args, **kwargs)

    @classmethod
    def update(cls, instance, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, instance, *args, **kwargs):
        instance.delete()
