
from rest_framework.permissions import IsAuthenticated


class IsAdminUser(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type == 'admin' and \
                super(IsAdminUser, self).has_permission(request, view):
            return True
        return False


class IsDriverUser(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type == 'driver' and \
                super(IsDriverUser, self).has_permission(request, view):
            return True
        return False


class IsRiderUser(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_anonymous and \
            request.user.user_type == 'rider' and \
                super(IsRiderUser, self).has_permission(request, view):
            return True
        return False
