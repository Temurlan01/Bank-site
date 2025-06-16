from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'phone_number',
            'password',
            'password2',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=6, max_length=20)
    password = serializers.CharField(min_length=8)