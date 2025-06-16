from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import CustomUser


class SendMoneyTests(APITestCase):
    def setUp(self):
        self.sender = CustomUser.objects.create_user(
            phone_number='111111', password='pass', balance=100)
        self.recipient = CustomUser.objects.create_user(
            phone_number='222222', password='pass', balance=0)
        self.amount = 50
        self.token = Token.objects.create(user=self.sender)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_send_money_success(self):
        data = {'phone_number': '222222', 'amount': 50}
        response = self.client.post('/api/v1/user/send-money/', data)
        self.assertEqual(response.status_code, 200)
        self.sender.refresh_from_db()
        self.recipient.refresh_from_db()
        self.assertEqual(response.json()['your_new_balance'], self.sender.balance)
        self.assertEqual(response.json()['recipient'],self.recipient.phone_number)
        self.assertEqual(response.json()['amount_sent'],
                         self.amount)
