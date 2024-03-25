from api.admin_panel.serializers import (
    DriverSerializer
)
from rest_framework.viewsets import ModelViewSet
from rides_app.models import User
from rides_app.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response


class DriverViewSet(ModelViewSet):
    queryset = User.objects.filter(user_type="driver", is_deleted=False)
    serializer_class = DriverSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "Successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
