from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bank.models import Transaction
from bank.serializers import (TransactionHistorySerializer,
                              SendMoneySerializer, UserSearchRequestSerializer,
                              UserBalanceSerializer, BalanceUpdateSerializer)
from django.db import models, transaction


class UserBalanceAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserBalanceSerializer

    def get(self, request):
        serializer = UserBalanceSerializer(request.user)
        return Response(serializer.data)



class UserSearchAPIView(GenericAPIView):
    """Вью для поиска пользователей"""
    serializer_class = UserSearchRequestSerializer
    def get(self, request):
        serializer = UserSearchRequestSerializer(data=request.query_params, context={'request': request})
        serializer.is_valid(raise_exception=True)
        users = serializer.validated_data['users']

        return Response([
            {'id': u.id, 'phone_number': u.phone_number}
            for u in users
        ])



class ClickButtonAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BalanceUpdateSerializer

    def post(self, request):
        user = request.user
        user.balance += 1
        user.save()

        serializer = BalanceUpdateSerializer({
            'phone_number': user.phone_number,
            'new_balance': user.balance,
        })

        return Response(serializer.data, status=200)



class SendMoneyAPIView(GenericAPIView):
    """Вью для отправки денег другим пользователям"""
    permission_classes = [IsAuthenticated]
    serializer_class = SendMoneySerializer

    def post(self, request):
        serializer = SendMoneySerializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)

        sender = request.user
        recipient = serializer.validated_data['recipient']
        amount = serializer.validated_data['amount']

        with transaction.atomic():
            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()

            Transaction.objects.create(
                sender=sender,
                recipient=recipient,
                amount=amount
            )

        return Response(status=200, data={
            'your_new_balance': sender.balance,
            'recipient': recipient.phone_number,
            'amount_sent': amount
        })



class TransactionHistoryAPIView(GenericAPIView):
    """Вью для историй транзакции"""
    permission_classes = [IsAuthenticated]
    serializer_class =TransactionHistorySerializer

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
