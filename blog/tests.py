from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from blog.models import User

# 创建临时数据库，并运行test
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username": 'okokoko', "email": "anyway@localhost.com",
                "password": '123456'}
        response = self.client.post('/blog/user/', data)
        print('ok', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="flyingbutton", email="474827656@qq.com",
                                             password='123456789')
        self.user.save()
        self.token = Token.objects.create(user__username='flyingbutton')
