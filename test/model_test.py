from rides_app.models import (
    Location,
    Ride,
    RideLiveLocation,
    DriverRequest
)
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'mobile': '1234567890',
            'user_type': 'driver',
            'password': '1111'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('1111'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.user_type, 'driver')

    def test_create_superuser(self):
        admin_data = {
            'email': 'admin@example.com',
            'password': 'admin'
        }
        admin = User.objects.create_superuser(**admin_data)
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.check_password('admin'))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.user_type, 'admin')


class LocationModelTest(TestCase):
    def test_create_location(self):
        location = Location.objects.create(
            latitude=12.34,
            longitude=56.78
        )
        self.assertIsNotNone(location)


class RideModelTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(
            email='rider@example.com',
            mobile='1234567892',
            password='password',
            user_type='rider'
        )
        self.driver = User.objects.create_user(
            email='driver@example.com',
            mobile='1234567891',
            password='password',
            user_type='driver'
        )
        self.pickup_location = Location.objects.create(
            latitude=12.34,
            longitude=56.78
        )
        self.drop_location = Location.objects.create(
            latitude=21.43,
            longitude=65.87
        )

    def test_create_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup_location,
            drop_location=self.drop_location
        )
        self.assertEqual(ride.status, 'pending')


class RideLiveLocationModelTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(
            email='rider@example.com',
            password='password',
            mobile='1234567890',
            user_type='rider'
        )
        self.driver = User.objects.create_user(
            email='driver@example.com',
            mobile='1234567891',
            password='password',
            user_type='driver'
        )
        self.pickup_location = Location.objects.create(
            latitude=12.34,
            longitude=56.78
        )
        self.drop_location = Location.objects.create(
            latitude=21.43,
            longitude=65.87
        )
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup_location,
            drop_location=self.drop_location
        )

    def test_create_ride_live_location(self):
        ride_live_location = RideLiveLocation.objects.create(
            ride=self.ride,
            latitude=12.34,
            longitude=56.78
        )
        self.assertIsNotNone(ride_live_location)


class DriverRequestModelTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(
            email='rider@example.com',
            mobile='1234567890',
            password='password',
            user_type='rider'
        )
        self.driver = User.objects.create_user(
            email='driver@example.com',
            password='password',
            mobile='1234567891',
            user_type='driver'
        )
        self.pickup_location = Location.objects.create(
            latitude=12.34,
            longitude=56.78
        )
        self.drop_location = Location.objects.create(
            latitude=21.43,
            longitude=65.87
        )
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup_location,
            drop_location=self.drop_location
        )

    def test_create_driver_request(self):
        driver_request = DriverRequest.objects.create(
            ride=self.ride,
            driver=self.driver
        )
        self.assertEqual(driver_request.status, 'pending')
