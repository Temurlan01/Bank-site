from rest_framework import serializers
from bank.models import Transaction
from users.models import CustomUser


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'phone_number',
            'balance'
        ]



class UserSearchRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        request_user = self.context['request'].user
        phone_number = data['phone_number']

        users = CustomUser.objects.filter(
            phone_number__icontains=phone_number
        ).exclude(id=request_user.id)

        if not users.exists():
            raise serializers.ValidationError({
                'phone_number': 'Пользователи не найдены или вы ищете самого себя'
            })

        data['users'] = users
        return data



class BalanceUpdateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(read_only=True)
    new_balance = serializers.IntegerField(read_only=True)



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
        fields = [
            'direction',
            'other_user',
            'amount',
            'timestamp'
        ]

    def get_direction(self, obj):
        request_user = self.context['request'].user

        mapping = {
            obj.sender_id: '-',
            obj.recipient_id: '+',
        }
        return mapping[request_user.id]



    def get_other_user(self, obj):
        user = self.context['request'].user

        if obj.sender == user:
            other_user = obj.recipient
        else:
            other_user = obj.sender

        return other_user.phone_number
