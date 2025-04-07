from celery import Celery

app = Celery(
    "payment_service",
)
app.config_from_object('django.conf:settings', namespace='CELERY')
