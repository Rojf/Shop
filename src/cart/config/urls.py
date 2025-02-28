from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from ..api.views import router

api = NinjaAPI(openapi_url="v1/cart/openapi.json", docs_url="v1/cart/docs")

api.add_router("v1/cart/", router)


urlpatterns = [
    path('v1/cart/admin/', admin.site.urls),
    path('v1/cart/__debug__/', include('debug_toolbar.urls')),
    path('', api.urls),
]
