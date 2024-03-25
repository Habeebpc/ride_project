from django.db import models

RIDING_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('started', 'Started'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
)

REQUEST_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected')
)


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
# this model is used to get user marked location for a ride


class Ride(models.Model):
    rider = models.ForeignKey(
        'rides_app.User',
        on_delete=models.CASCADE,
        related_name='rider_riders'
    )
    driver = models.ForeignKey(
        'rides_app.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ride_drivers'
    )
    pickup_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ride_pickups'
    )
    drop_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ride_drops'
    )
    status = models.CharField(
        max_length=20,
        choices=RIDING_STATUS,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RideLiveLocation(models.Model):
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='live_locations'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
# purpose of above model is to fetch live location of a ride


class DriverRequest(models.Model):
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='driver_requests'
    )
    driver = models.ForeignKey(
        'rides_app.User',
        on_delete=models.CASCADE,
        related_name='driver_requests'
    )
    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default='pending'
    )


""" purpose of above model is to accept or reject a ride request.
 if a  driver accept the request then he will be assigned to the ride.
  and at the same time delete all other request for the same ride """
