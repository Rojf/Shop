from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from api.views import router, admin_order_pdf, admin_order_detail


api = NinjaAPI()

api.add_router("orders/", router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', admin_order_pdf, name='admin_order_pdf'),
    path('api/v1/', api.urls),
]
