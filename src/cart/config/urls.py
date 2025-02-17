from api.views import router
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

api = NinjaAPI(openapi_url="api/v1/cart/openapi.json", docs_url="api/v1/cart/docs")

api.add_router("api/v1/cart/", router)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', api.urls),
]
