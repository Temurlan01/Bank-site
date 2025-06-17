from rest_framework.test import APITestCase
from users.models import CustomUser
from bank.models import Transaction
from rest_framework.authtoken.models import Token


class TransactionHistoryTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            phone_number='1111111111', password='pass', balance=100
        )
        self.user2 = CustomUser.objects.create_user(
            phone_number='2222222222', password='pass', balance=100
        )
        Transaction.objects.create(sender=self.user1, recipient=self.user2, amount=50)

        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_transaction_history(self):
        response = self.client.get('/api/v1/user/transactions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        transaction = response.json()[0]

        self.assertEqual(transaction['amount'], 50)
        self.assertEqual(transaction['direction'], '-')
        self.assertEqual(transaction['other_user'], self.user2.phone_number)