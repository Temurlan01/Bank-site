from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from bank.models import Transaction
from bank.serializers import UserSearchSerializer, TransactionHistorySerializer
from users.models import CustomUser
from django.db import models


class UserBalanceAPIView(APIView):
    """Вью, для отображение информации о балансе"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        return Response({
            "phone_number": user.phone_number,
            "balance": user.balance,
            "token": token.key
        })



class UserSearchAPIView(APIView):
    """Вью для поиска пользователей"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response(status=400, data={
                'message': 'Номер телефона обязателен'
            })
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response(status=404, data={
                'message': 'Пользователь не найден'
            })

        if user == request.user:
            return Response(status=400, data={
                'error': 'Нельзя искать самого себя'
            })

        serializer = UserSearchSerializer(user)
        return Response(serializer.data)



class ClickButtonAPIView(APIView):
    """Вью для кнопки увеличение баланса"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.balance += 1
        user.save()
        return Response(status=200, data={
            'phone_number': user.phone_number,
            'message': 'Баланс увеличен на 1',
            'new_balance': user.balance,
        })



class SendMoneyAPIView(APIView):
    """Вью для отправки денег другим пользователям """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        balance = request.data.get('balance')

        if not phone_number or not balance:
            return Response(status=400, data={
                'message': 'Номер и сумма обязательны'
            })

        try:
            balance = int(balance)
            if balance <= 0:
                return Response(status=400, data={
                    'message': 'Сумма должна быть положительной'
                })
        except ValueError:
            return Response(status=400, data={
                'message': 'Сумма должна быть числом'
            })

        try:
            recipient = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response(status=404, data={
                'message': 'Получатель не найден'
            })

        sender = request.user

        if sender == recipient:
            return Response(status=400, data={
                'message': 'Нельзя отправить деньги самому себе'
            })

        if sender.balance < balance:
            return Response(status=400, data={
                'message': 'Недостаточно средств'
            })

        sender.balance -= balance
        recipient.balance += balance
        sender.save()
        recipient.save()

        Transaction.objects.create(
            sender=sender,
            recipient=recipient,
            amount=balance
        )

        return Response(status=200, data={
            'message': f'Вы отправили {balance} пользователю {recipient.phone_number}',
            'your_new_balance': sender.balance,
            'recipient': recipient.phone_number,
            'balance_sent': balance
        })



class TransactionHistoryAPIView(APIView):
    """Вью для историй транзакции"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        ).order_by('-timestamp')

        serializer = TransactionHistorySerializer(
            transactions,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)