from rest_framework import serializers
from rides_app. models import (
    DriverLocationTracker,
    DriverRequest,
    User,
    Location,
    Ride,
    RideLiveLocation
)
from django.shortcuts import get_object_or_404


class DriverLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocationTracker
        fields = ('latitude', 'longitude')


class RiderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile')


class LocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')


class RideRequestListSerializer(serializers.ModelSerializer):
    rider = serializers.SerializerMethodField()
    pickup_location = serializers.SerializerMethodField()
    drop_location = serializers.SerializerMethodField()

    class Meta:
        model = DriverRequest
        fields = ('id', 'rider', 'pickup_location', 'drop_location')

    def get_rider(self, obj):
        return RiderDataSerializer(obj.ride.rider).data

    def get_pickup_location(self, obj):
        return LocationDataSerializer(obj.ride.pickup_location).data

    def get_drop_location(self, obj):
        return LocationDataSerializer(obj.ride.drop_location).data


class RideRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRequest
        fields = ('status',)

    def update(self, instance, validated_data):
        status = validated_data['status']
        if status == 'accepted':
            instance.ride.driver = instance.driver
            instance.ride.status = 'accepted'
            instance.ride.save()
            DriverRequest.objects.filter(
                ride=instance.ride).exclude(
                id=instance.id).update(status='rejected')
        elif status == 'rejected':
            if not DriverRequest.objects.filter(
                    ride=instance.ride,
                    status__in=['accepted', 'pending']).exclude(
                    id=instance.id).exists():
                instance.ride.status = 'cancelled'
                instance.ride.save()

        return super().update(instance, validated_data)


"""
if a driver accept a request then the ride assign to the driver and status of
ride change to accepted. also at the same time reject all the ride request for
 the same ride. if a driver reject a request then check there is any other
non rejected requests for this ride if not then change the ride status to
cancelled.

"""


class RideListSerializer(serializers.ModelSerializer):
    pickup_location = LocationDataSerializer('pickup_location')
    drop_location = LocationDataSerializer('drop_location')

    class Meta:
        model = Ride
        fields = (
            'id',
            'pickup_location',
            'drop_location',
            'status',
            'created_at'
        )


class RideDetailSerializer(serializers.ModelSerializer):
    rider = RiderDataSerializer('rider')
    pickup_location = LocationDataSerializer('pickup_location')
    drop_location = LocationDataSerializer('drop_location')

    class Meta:
        model = Ride
        fields = (
            'rider',
            'pickup_location',
            'drop_location',
            'status',
            'created_at',
        )


class RideStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('status',)


class RideLocationTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideLiveLocation
        fields = ('latitude', 'longitude')

    def create(self, validated_data):
        ride = get_object_or_404(Ride, id=self.context['ride_id'])
        validated_data['ride'] = ride
        return super().create(validated_data)
