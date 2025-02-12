from django.urls import path

from . import webhooks

urlpatterns = [
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
