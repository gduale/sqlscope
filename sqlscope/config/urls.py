from django.contrib import admin
from django.urls import path, include

from sqlscope import urls

urlpatterns = [
    path('', include('sqlscope.urls')),
    path('admin/', admin.site.urls),
]
