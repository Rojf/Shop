"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# pylint: disable=E0611

from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from api.views import router

api = NinjaAPI(openapi_url="v1/catalog/openapi.json", docs_url="v1/catalog/docs")
api.add_router("v1/catalog", router)

urlpatterns = [
    path('v1/catalog/admin/', admin.site.urls),
    path('v1/catalog/__debug__/', include('debug_toolbar.urls')),
    path('', api.urls),
]
