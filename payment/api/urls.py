from django.urls import path

from . import webhooks


app_name = 'payment'

urlpatterns = [
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
