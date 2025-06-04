from rest_framework import serializers
from bank.models import Transaction
from users.models import CustomUser


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number',]



class TransactionHistorySerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['direction', 'other_user', 'amount', 'timestamp']

    def get_direction(self, obj):
        request_user = self.context['request'].user
        if obj.sender == request_user:
            return '-'
        elif obj.recipient == request_user:
            return '+'
        return ''

    def get_other_user(self, obj):
        request_user = self.context['request'].user
        return (
            obj.recipient.phone_number if obj.sender == request_user
            else obj.sender.phone_number
        )