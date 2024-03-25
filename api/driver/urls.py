from django.urls import path
from .views import (
    DriverLocationUpdateView,
    RideRequestListView,
    RideRequestStatusView,
    RideViewSet,
    RideDetailView,
    RideLocationTrackView
)

urlpatterns = [
    path('live-location/',
         DriverLocationUpdateView.as_view({'get': 'retrieve',
                                           'put': 'update'})),
    path('ride-requests/', RideRequestListView.as_view({'get': 'list'})),
    path('ride-request/<int:pk>/status/',
         RideRequestStatusView.as_view({'put': 'update'})),
    path('rides/', RideViewSet.as_view({'get': 'list'})),
    path('ride/<int:pk>/', RideDetailView.as_view({'get': 'retrieve',
                                                   'put': 'update'})),
    path('ride/<int:pk>/live-location/',
         RideLocationTrackView.as_view({'post': 'create'})),
]
