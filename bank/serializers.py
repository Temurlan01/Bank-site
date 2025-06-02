from rest_framework import serializers
from users.models import CustomUser


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number',]