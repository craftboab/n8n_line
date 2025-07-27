from django.urls import path
from . import views

app_name = 'linebot_app'

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
] 