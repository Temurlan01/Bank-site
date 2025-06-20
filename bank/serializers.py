from rest_framework import serializers
from bank.models import Transaction
from users.models import CustomUser

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'balance']

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number',]



class UserSearchRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
 
    def validate(self, data):
        request_user = self.context['request'].user
        phone_number = data['phone_number']

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'phone_number': 'Пользователь не найден'})

        if user == request_user:
            raise serializers.ValidationError({'phone_number': 'Нельзя искать самого себя'})

        data['user'] = user
        return data



class SendMoneySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)

    def validate(self, data):
        sender = self.context['request'].user
        amount = data['amount']
        phone_number = data['phone_number']

        try:
            recipient = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'phone_number': 'Получатель не найден'})

        if sender == recipient:
            raise serializers.ValidationError({'phone_number': 'Нельзя отправить деньги самому себе'})

        if sender.balance < amount:
            raise serializers.ValidationError({'amount': 'Недостаточно средств для перевода'})

        data['recipient'] = recipient
        return data



class TransactionHistorySerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['direction', 'other_user', 'amount', 'timestamp']

    def get_direction(self, obj):
        request_user = self.context['request'].user

        # alternative way
        # mapping = {
        #     obj.sender_id: '-',
        #     obj.recipient_id: '+',
        # }
        # return mapping[request_user.id]

        if obj.sender == request_user:
            return '-'
        elif obj.recipient == request_user:
            return '+'
        return ''

    def get_other_user(self, obj):
        user = self.context['request'].user

        if obj.sender == user:
            other_user = obj.recipient
        else:
            other_user = obj.sender

        return other_user.phone_number
