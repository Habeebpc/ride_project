from django.urls import path
from .views import (
    DriverViewSet
)

urlpatterns = [
    path('drivers/', DriverViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('drivers/<int:pk>/',
         DriverViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
