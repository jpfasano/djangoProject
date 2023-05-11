

from django.urls import path
# from . import views
from .views import (
    RoutesListView,
    RoutesDetailView,
    RoutesCreateView,
    RoutesUpdateView,
    RoutesDeleteView,
    UserRoutesListView
)

urlpatterns = [
    # path('routes/', views.routes, name='routes'),

    path('', RoutesListView.as_view(), name='routes'),
    path('user/<str:username>', UserRoutesListView.as_view(), name='user-routes'),
    path('<int:pk>/', RoutesDetailView.as_view(), name='route-detail'),
    path('new/', RoutesCreateView.as_view(), name='route-create'),
    path('<int:pk>/update', RoutesUpdateView.as_view(), name='route-update'),
    path('<int:pk>/delete', RoutesDeleteView.as_view(), name='route-delete'),
]
