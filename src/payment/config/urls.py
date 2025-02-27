from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from ..api.views import router as api_router
from ..api.webhooks import router as webhook_router

api = NinjaAPI(openapi_url="v1/payment/openapi.json", docs_url="v1/payment/docs")
api.add_router("v1/payment/", api_router)
api.add_router("v1/payment/webhook/", webhook_router)


urlpatterns = [path('v1/payment/admin/', admin.site.urls), path('', api.urls)]
