from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from api.views import admin_order_detail, admin_order_pdf, router

api = NinjaAPI(openapi_url="v1/orders/openapi.json", docs_url="v1/orders/docs")

api.add_router("v1/orders/", router)

urlpatterns = [
    path('v1/orders/admin/', admin.site.urls),
    path(
        'v1/orders/admin/order/<int:order_id>/',
        admin_order_detail,
        name='admin_order_detail',
    ),
    path(
        'v1/orders/admin/order/<int:order_id>/pdf/',
        admin_order_pdf,
        name='admin_order_pdf',
    ),
    path('', api.urls),
]
