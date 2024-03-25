from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('system_admin/', include('api.admin_panel.urls')),
    path('rider/', include('api.rider.urls')),
    path('driver/', include('api.driver.urls'))
]
