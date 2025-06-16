from rest_framework.test import APITestCase
from users.models import CustomUser


class RegistrationAPITest(APITestCase):
    def test_registration(self):
        data = {
            'phone_number': '123456789',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post('/api/v1/users/register/', data)
        self.assertEqual(201, response.status_code)



class LoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='123456789', password='testpassword')

    def test_login(self):
        data = {
            'phone_number': '123456789',
            'password': 'testpassword'
        }
        response = self.client.post('/api/v1/users/login/', data)
        self.assertEqual(200, response.status_code)
