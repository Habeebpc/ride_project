from rest_framework import serializers
from rides_app.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'name',
            'mobile',
            'email',
            'password'
        )

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if (len(mobile) > 12 or not mobile.isdigit()):
            raise serializers.ValidationError('Invalid mobile number')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['user_type'] = 'rider'
        user = User.objects.create_user(**validated_data)
        return user
