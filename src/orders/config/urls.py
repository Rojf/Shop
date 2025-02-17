# pylint: disable=E0611

from api.views import admin_order_detail, admin_order_pdf, router
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(openapi_url="api/v1/orders/openapi.json", docs_url="api/v1/orders/docs")

api.add_router("api/v1/orders/", router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', admin_order_pdf, name='admin_order_pdf'),
    path('', api.urls),
]
