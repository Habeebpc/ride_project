from django.urls import path
from .views import (
    LoginApiView,
    SignUpApiView
)

urlpatterns = [
    path('signup/', SignUpApiView.as_view({'post': 'create'}), name='signup'),
    path('login/', LoginApiView.as_view({'post': 'create'}), name='login'),
]
