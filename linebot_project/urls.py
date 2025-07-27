"""
URL configuration for linebot_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('linebot/', include('linebot_app.urls')),
] 