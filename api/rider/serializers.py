from rest_framework import serializers
from rides_app.models import (
    Ride,
    Location,
    User,
    DriverLocationTracker,
    DriverRequest,
    RideLiveLocation
)
from geopy.distance import distance


def find_nearest_drivers(latitude, longitude):
    starting_point = (float(latitude), float(longitude))
    drivers = User.objects.filter(user_type='driver', is_deleted=False)
    nearest_drivers = []
    for i in range(1, 11):
        if drivers and nearest_drivers == []:
            for driver in drivers:
                current_location = DriverLocationTracker.objects.get(
                    driver=driver)
                driver_point = (current_location.latitude,
                                current_location.longitude)
                if distance(starting_point, driver_point).km <= i:
                    nearest_drivers.append(driver)
    else:
        return nearest_drivers


"""
The function initially attempts to find drivers within 1 km distance.
If any drivers are found, they are returned as a list.
If no drivers are found, the distance limit is increased to 2 km,
and the same process is repeated up to a maximum distance of 10 km.
If no drivers are found within the maximum distance, an empty list is returned.

"""


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')


class RideBookingSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer()
    drop_location = LocationSerializer()

    class Meta:
        model = Ride
        fields = ('pickup_location', 'drop_location')

    def validate(self, attrs):
        pickup_location = attrs.get('pickup_location')
        self.nearest_drivers = find_nearest_drivers(
            pickup_location['latitude'],
            pickup_location['longitude']
        )
        if self.nearest_drivers == []:
            raise serializers.ValidationError('No nearby drivers found')
        return super().validate(attrs)

    def create(self, validated_data):
        pickup_location = Location.objects.create(
            latitude=validated_data['pickup_location']['latitude'],
            longitude=validated_data['pickup_location']['longitude']
        )

        drop_location = Location.objects.create(
            latitude=validated_data['drop_location']['latitude'],
            longitude=validated_data['drop_location']['longitude']
        )
        rider = self.context['request'].user
        ride = Ride.objects.create(
            rider=rider,
            pickup_location=pickup_location,
            drop_location=drop_location
        )

        driver_requests = []
        for driver in self.nearest_drivers:
            obj = DriverRequest(
                driver=driver,
                ride=ride
            )
            driver_requests.append(obj)
        DriverRequest.objects.bulk_create(driver_requests)
        return ride

    def to_representation(self, instance):
        return {'message': 'booking request sent to nearest drivers in your area'}


"""
its better to run this driver request creation code in a celery task or thread
"""


class RideBookingListSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer('pickup_location')
    drop_location = LocationSerializer('drop_location')

    class Meta:
        model = Ride
        fields = (
            'id',
            'pickup_location',
            'drop_location',
            'status',
            'created_at'
        )


class RideBookingDetailSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer('pickup_location')
    drop_location = LocationSerializer('drop_location')
    location_tracer = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = (
            'id',
            'pickup_location',
            'drop_location',
            'status',
            'created_at',
            'driver',
            'location_tracer',
        )

    def get_location_tracer(self, obj):
        return RideLiveLocation.objects.filter(ride=obj).values_list(
            'latitude',
            'longitude',
            'updated_at'
        ).order_by('updated_at')
