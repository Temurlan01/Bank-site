from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import CustomUser


class UserSearchTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number=111111, password="password"
        )
        self.other_user = CustomUser.objects.create_user(
            phone_number=222222, password="password"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_search_other_user(self):
        response = self.client.get('/api/v1/user/search/?phone_number=222222')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.other_user.id)
        self.assertEqual(response.json()['phone_number'], self.other_user.phone_number)

    def test_user_search_self(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get('/api/v1/user/search/?phone_number=1111111111')
        self.assertEqual(response.status_code, 400)
