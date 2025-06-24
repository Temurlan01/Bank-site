from rest_framework.test import APITestCase
from users.models import CustomUser
from rest_framework.authtoken.models import Token


class BalanceTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='1111111111', password='pass', balance=150)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_balance(self):
        response = self.client.get('/api/v1/user/balance/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['balance'], 150)
        self.assertEqual(response.json()['phone_number'],
                         self.user.phone_number)

    def test_balance_unauthorized(self):
        response = self.client.get("/api/v1/user/balance/")
        self.assertEqual(response.status_code, 401)
