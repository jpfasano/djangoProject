from django.urls import path
# from . import views
from .views import (
    RidesListView,
    RidesDetailView,
    RidesCreateView,
    RidesUpdateView,
    RidesDeleteView,
    UserRidesListView
)

urlpatterns = [
    # path('rides/', views.rides, name='rides'),
    path('', RidesListView.as_view(), name='rides'),
    path('user/<str:username>/', UserRidesListView.as_view(), name='user-rides'),
    path('<int:pk>/', RidesDetailView.as_view(), name='ride-detail'),
    path('new/', RidesCreateView.as_view(), name='ride-create'),
    path('<int:pk>/update/', RidesUpdateView.as_view(), name='ride-update'),
    path('<int:pk>/delete/', RidesDeleteView.as_view(), name='ride-delete'),
]