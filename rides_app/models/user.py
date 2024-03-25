from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

from django.dispatch import receiver
from django.db.models.signals import post_save


USER_TYPES = (
    ('admin', 'Admin'),
    ('rider', 'Rider'),
    ('driver', 'Driver')
)


def validate_unique_mobile_number(value):
    if len(value) > 12 or len(value) < 10 or not value.isdigit():
        raise ValidationError('Invalid mobile number.')


class Manager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("you have not given email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", 'admin')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(
        max_length=12,
        validators=[validate_unique_mobile_number],
        unique=True
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = Manager()

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_driver_location_tracker(sender, instance, created, **kwargs):
    if instance.user_type == 'driver' and created:
        DriverLocationTracker.objects.create(driver=instance)


class DriverLocationTracker(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
