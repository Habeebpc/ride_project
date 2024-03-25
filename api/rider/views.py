from api.rider.serializers import (
    RideBookingSerializer,
    RideBookingListSerializer,
    RideBookingDetailSerializer
)
from rest_framework.viewsets import ModelViewSet
from rides_app.models import Ride
from rides_app.permissions import IsRiderUser
from django_filters.rest_framework import DjangoFilterBackend


class RideBookingViewSet(ModelViewSet):
    permission_classes = [IsRiderUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status',]

    def get_queryset(self):
        return Ride.objects.filter(rider=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RideBookingListSerializer
        return RideBookingSerializer

    def get_serializer_context(self):
        return {
            "request": self.request
        }


class RideBookingDetailView(ModelViewSet):
    serializer_class = RideBookingDetailSerializer
    permission_classes = [IsRiderUser]
    queryset = Ride.objects.all()
