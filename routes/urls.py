

from django.urls import path
from . import views
from .views import (
    RoutesListView,
    RoutesDetailView,
    RoutesCreateView,
    RoutesUpdateView,
    RoutesDeleteView,
    UserRoutesListView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='routes-about'),
    # path('routes/', views.routes, name='routes'),
    path('routes', RoutesListView.as_view(), name='routes'),
    path('user/<str:username>', UserRoutesListView.as_view(), name='user-routes'),
    path('routes/<int:pk>/', RoutesDetailView.as_view(), name='route-detail'),
    path('routes/new/', RoutesCreateView.as_view(), name='route-create'),
    path('routes/<int:pk>/update', RoutesUpdateView.as_view(), name='route-update'),
    path('routes/<int:pk>/delete', RoutesDeleteView.as_view(), name='route-delete'),
]
