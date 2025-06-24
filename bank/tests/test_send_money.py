from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import CustomUser


class SendMoneyTests(APITestCase):
    def setUp(self):
        self.sender = CustomUser.objects.create_user(
            phone_number='111111', password='pass', balance=100)
        self.recipient = CustomUser.objects.create_user(
            phone_number='222222', password='pass', balance=0)
        self.token = Token.objects.create(user=self.sender)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_send_money_success(self):
        data = {
            'phone_number': '222222',
            'amount': 50
        }
        response = self.client.post('/api/v1/user/send-money/', data)
        self.assertEqual(response.status_code, 200)
        self.sender.refresh_from_db()
        self.recipient.refresh_from_db()
        self.assertEqual(response.json()['your_new_balance'], 50)
        self.assertEqual(response.json()['recipient'], self.recipient.phone_number)
        self.assertEqual(response.json()['amount_sent'], 50)
        self.assertEqual(self.sender.balance, 50)
        self.assertEqual(self.recipient.balance, 50)

    def test_send_money_not_authenticated(self):
        self.client.credentials()
        data = {
            'phone_number': '222222',
            'amount': 50
        }
        response = self.client.post('/api/v1/user/send-money/', data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)

    def test_send_money_to_nonexistent_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "phone_number": "9999999999",
            "amount": 10
        }
        response = self.client.post("/api/v1/user/send-money/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone_number', response.data)
        self.assertIn('Получатель не найден', response.data['phone_number'][0])

    def test_send_money_to_self(self):
        data = {
            "phone_number": self.sender.phone_number,
            "amount": 10
        }
        response = self.client.post("/api/v1/user/send-money/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone_number', response.data)
        self.assertIn('Нельзя отправить деньги самому себе', response.data['phone_number'][0])

    def test_send_money_unauthenticated(self):
        self.client.credentials()  # сбрасываем токен
        data = {
            "phone_number": self.recipient.phone_number,
            "amount": 10
        }
        response = self.client.post("/api/v1/user/send-money/", data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)

# TDD посмотри что это такое и для чего используется
