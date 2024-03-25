from django.urls import path
from .views import (
    RideBookingViewSet,
    RideBookingDetailView
)

urlpatterns = [
    path('bookings/',
         RideBookingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('booking/<int:pk>/',
         RideBookingDetailView.as_view({'get': 'retrieve', })),
]
