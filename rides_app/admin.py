from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rides_app.models import (
    User,
    DriverLocationTracker,
    Location,
    Ride,
    RideLiveLocation,
    DriverRequest,
)


class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'),
         {'fields': ('name', 'mobile', 'user_type')}),
        (('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser', 'is_deleted')}),
    )

    list_display = ('id', 'name', 'email', 'mobile', 'user_type')
    ordering = ('id',)
    list_filter = ('user_type',)
    search_fields = ('name', 'email', 'mobile', 'user_type')


class DriverLocationTrackerAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'latitude', 'longitude')
    ordering = ('id',)
    list_filter = ('driver',)


class DriverRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'ride', 'status')
    ordering = ('id',)


class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(DriverLocationTracker, DriverLocationTrackerAdmin)
admin.site.register(DriverRequest, DriverRequestAdmin)
admin.site.register(Ride, RideAdmin)
