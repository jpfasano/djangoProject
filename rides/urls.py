from django.urls import path
from . import views
from .views import (
    # RidesListView,
    RidesDetailView,
    RidesCreateView,
    RidesUpdateView,
    RidesDeleteView,
    UserRidesListView, ScheduledRides, CompletedRides, RidesReportUpdateView
)

urlpatterns = [

    path('', ScheduledRides.as_view(), name='home'),
    path('about/', views.about, name='routes-about'),
    # path('rides/', views.rides, name='rides'),
    path('completed-rides/', CompletedRides.as_view(), name='completed-rides'),
    path('rides/user/<str:username>/', UserRidesListView.as_view(), name='user-rides'),
    path('rides/<int:pk>/', RidesDetailView.as_view(), name='ride-detail'),
    path('rides/new/', RidesCreateView.as_view(), name='ride-create'),
    path('rides/<int:pk>/new-report/', RidesReportUpdateView.as_view(), name='ride-report-update'),
    path('rides/<int:pk>/update/', RidesUpdateView.as_view(), name='ride-update'),
    path('rides/<int:pk>/delete/', RidesDeleteView.as_view(), name='ride-delete'),
]