from api.driver.serializers import (
    DriverLocationUpdateSerializer,
    RideRequestListSerializer,
    RideRequestStatusSerializer,
    RideListSerializer,
    RideDetailSerializer,
    RideStatusUpdateSerializer,
    RideLocationTrackSerializer

)
from rest_framework.viewsets import ModelViewSet
from rides_app.models import (
    DriverLocationTracker,
    DriverRequest,
    Ride
)
from rides_app.permissions import IsDriverUser


class DriverLocationUpdateView(ModelViewSet):
    serializer_class = DriverLocationUpdateSerializer
    queryset = DriverLocationTracker.objects.all()
    permission_classes = [IsDriverUser]

    def get_object(self):
        return self.request.user.driverlocationtracker


"""
This API is mandatory to track each drivers current location.
 so this api need to call in a specific interval.

"""


class RideRequestListView(ModelViewSet):
    serializer_class = RideRequestListSerializer
    permission_classes = [IsDriverUser]

    def get_queryset(self):
        return DriverRequest.objects.filter(
            driver=self.request.user, status='pending')


class RideRequestStatusView(ModelViewSet):
    serializer_class = RideRequestStatusSerializer
    queryset = DriverRequest.objects.all()
    permission_classes = [IsDriverUser]


class RideViewSet(ModelViewSet):
    permission_classes = [IsDriverUser]
    serializer_class = RideListSerializer

    def get_queryset(self):
        return Ride.objects.filter(driver=self.request.user)


class RideDetailView(ModelViewSet):
    serializer_class = RideDetailSerializer
    permission_classes = [IsDriverUser]
    queryset = Ride.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RideDetailSerializer
        return RideStatusUpdateSerializer


class RideLocationTrackView(ModelViewSet):
    serializer_class = RideLocationTrackSerializer
    permission_classes = [IsDriverUser]

    def get_serializer_context(self):
        return {'ride_id': self.kwargs.get('pk')}
