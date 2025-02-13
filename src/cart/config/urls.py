from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from ..api.views import router

api = NinjaAPI()

api.add_router("v1/", router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/', api.urls),
]
