from rest_framework.test import APITestCase
from users.models import CustomUser


class RegistrationAPITest(APITestCase):
    def test_registration(self):
        data = {
            'phone_number': '123456789',
            'password': '12345678',
            'password2': '12345678'
        }
        response = self.client.post('/api/v1/users/register/', data)
        self.assertEqual(201, response.status_code)

    def test_register_passwords_do_not_match(self):
        data = {
            'phone_number': '2222222222',
            'password': 'pass1234',
            'password2': 'pass4321'
        }
        response = self.client.post("/api/v1/users/register/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Пароли не совпадают", str(response.data))



class LoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='123456789', password='12345678')

    def test_login(self):
        data = {
            'phone_number': '123456789',
            'password': '12345678'
        }
        response = self.client.post('/api/v1/users/login/', data)
        self.assertEqual(200, response.status_code)

    def test_login_with_wrong_password(self):
        data = {
            'phone_number': '1111111111',
            'password': 'wrongpass'
        }
        response = self.client.post("/api/v1/users/login/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Неверный номер или пароль", str(response.data))
