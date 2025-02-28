from django.db.models import Model

from utils.base_repository import BaseRepository

from .models import Payment, Refund


class PaymentRepository(BaseRepository):
    model = Payment

    @classmethod
    def get(cls, *args, **kwargs) -> Model | None:
        select_related = kwargs.pop('select_related', [])
        prefetch_related = kwargs.pop('prefetch_related', [])

        try:
            return (
                cls.model.objects.select_related(*select_related)
                .prefetch_related(*prefetch_related)
                .get(*args, **kwargs)
            )
        except cls.model.DoesNotExist:
            return None


class RefundRepository(BaseRepository):
    model = Refund
