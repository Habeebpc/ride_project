from rest_framework import serializers
from rides_app.models import User


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'mobile')

    def create(self, validated_data):
        validated_data['user_type'] = 'driver'
        validated_data['password'] = '1111'
        return User.objects.create_user(**validated_data)


"""we can generate random password and send to email.
but here in this test project we are using static password 1111 """
