

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='routes-about'),
    path('routes/', views.routes, name='routes'),
]
