from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

from .models import User


class AccountsTests(APITestCase):
    def setUp(self):
        # urls
        self.url_list = reverse('user-list')

        # create fake user 1
        self.test_user1 = User.objects.create(email = 'user1@user.ru', first_name = 'user1', last_name = 'user1', is_active = True, is_staff = True)
        self.test_user1.set_password('user')
        self.test_user1.save()
        # get token for user 1
        Token.objects.create(user = self.test_user1)
        self.test_user1_token = Token.objects.get(user__email = 'user1@user.ru')

        # create fake user 2
        self.test_user2 = User.objects.create(email = 'user2@user.ru', first_name = 'user2', last_name = 'user2', is_active = True, is_staff = True)
        self.test_user2.set_password('user')
        self.test_user2.save()
        # get token for user 2
        Token.objects.create(user = self.test_user2)
        self.test_user2_token = Token.objects.get(user__email = 'user2@user.ru')

        # create fake user 3
        self.test_user3 = User.objects.create(email = 'user3@user.ru', first_name = 'user3', last_name = 'user3', is_active = True, is_staff = True)
        self.test_user3.set_password('user')
        self.test_user3.save()
        # get token for user 3
        Token.objects.create(user = self.test_user3)
        self.test_user3_token = Token.objects.get(user__email = 'user3@user.ru')

    def test_get_user_list(self):
        # test get user list (non auth)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        # test get user list (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.client.logout()

    def test_post_user_list(self):
        # test create new user (non auth)
        data = {'email': 'fake1@fake.ru', 'password': 'fake1234'}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test create new user (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'email': 'fake2@fake.ru', 'password': 'fake1234'}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_error_post_user_list(self):
        # test create new user (invalid email)
        data = {'email': 'fake3', 'password': 'fake1234'}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test create new user (invalid password)
        data = {'email': 'fake3@fake.ru', 'password': 'fake'}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test create new user (repeat email)
        data = {'email': 'fake1@fake.ru', 'password': 'fake1234'}
        response = self.client.post(self.url_list, data = data)
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_detail(self):
        # test get user detail (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('user-detail', kwargs = {'pk': self.test_user1.id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_error_get_user_detail(self):
        # test get user detail (non auth)
        url_detail = reverse('user-detail', kwargs = {'pk': self.test_user1.id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test get user detail (invalid pk)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('user-detail', kwargs = {'pk': 0})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
