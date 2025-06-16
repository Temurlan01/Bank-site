from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from bank.models import Transaction
from bank.serializers import UserSearchSerializer, \
    TransactionHistorySerializer, SendMoneySerializer, \
    UserSearchRequestSerializer
from django.db import models, transaction


class UserBalanceAPIView(APIView):
    """Вью для, отображение информации о балансе"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "phone_number": user.phone_number,
            "balance": user.balance,
        })



class UserSearchAPIView(APIView):
    """Вью для поиска других пользователей"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSearchRequestSerializer(
            data=request.query_params,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        response_serializer = UserSearchSerializer(user)
        return Response(response_serializer.data)



class ClickButtonAPIView(APIView):
    """Вью для кнопки увеличение баланса"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.balance += 1
        user.save()
        return Response(
            status=200,
            data={
                'phone_number': user.phone_number,
                'new_balance': user.balance,
            },
        )



class SendMoneyAPIView(APIView):
    """Вью для отправки денег другим пользователям"""
    permission_classes = [IsAuthenticated]

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
