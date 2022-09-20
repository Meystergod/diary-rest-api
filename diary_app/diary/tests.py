from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from account.models import User

from .models import Diary


class DiariesTests(APITestCase):
    def setUp(self):
        # urls
        self.url_list = reverse('diary-list')

        # create fake user 1
        self.test_user1 = User.objects.create(email = 'user1@user.ru', first_name = 'user1', last_name = 'user1', is_active = True, is_staff = False)
        self.test_user1.set_password('user')
        self.test_user1.save()
        # get token for user 1
        Token.objects.create(user = self.test_user1)
        self.test_user1_token = Token.objects.get(user__email = 'user1@user.ru')

        # create fake user 2
        self.test_user2 = User.objects.create(email = 'user2@user.ru', first_name = 'user2', last_name = 'user2', is_active = True, is_staff = False)
        self.test_user2.set_password('user')
        self.test_user2.save()
        # get token for user 2
        Token.objects.create(user = self.test_user2)
        self.test_user2_token = Token.objects.get(user__email = 'user2@user.ru')

        # create fake diaries
        self.diary_test1 = Diary.objects.create(title = 'diary 1 user 1', kind = 'public', user = self.test_user1)
        self.diary_test2 = Diary.objects.create(title = 'diary 2 user 1', kind = 'public', user = self.test_user1)
        self.diary_test3 = Diary.objects.create(title = 'diary 1 user 2', kind = 'public', user = self.test_user2)
        self.diary_test4 = Diary.objects.create(title = 'diary 2 user 2', kind = 'public', user = self.test_user2)

    def test_get_diary_list(self):
        # test get diary list (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.client.logout()

    def test_error_get_diary_list(self):
        # test get diary list (non auth)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')

    def test_post_diary_list(self):
        # test create new diary (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'title': 'diary', 'kind': 'public'}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        # test create new diary (fake user)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'title': 'diaryfake', 'kind': 'public', 'user': self.test_user2.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.test_user1.id)
        self.client.logout()

    def test_error_post_diary_list(self):
        # test create new diary (non auth)
        data = {'title': 'diary', 'kind': 'public', 'user': self.test_user1.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test create new diary (invalid title)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'title': '', 'kind': 'public', 'user': self.test_user1.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        # test create new diary (invalid kind)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'title': 'diary', 'kind': ''}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        # test create new diary (repeat title)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'title': 'diary', 'kind': 'public'}
        response = self.client.post(self.url_list, data = data)
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_get_diary_detail(self):
        # test get diary detail (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_error_get_diary_detail(self):
        # test get diary detail (non auth)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test get diary detail (invalid pk)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': 0})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()

    def test_put_diary_detail(self):
        # test update diary (with permissions) (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        data = {'title': 'diary 1 user 1 updated', 'kind': 'public'}
        response = self.client.put(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'diary 1 user 1 updated')
        self.client.logout()

    def test_error_put_diary_detail(self):
        # test update diary (non auth)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        data = {'title': 'diary 1 user 1 updated', 'kind': 'public'}
        response = self.client.put(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test update diary (without permissions)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test3.id})
        data = {'title': 'diary 1 user 1 updated', 'kind': 'public'}
        response = self.client.put(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'У вас недостаточно прав для выполнения данного действия.')
        self.client.logout()
        # test update diary (invalid pk)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': 0})
        data = {'title': 'diary 1 user 1 updated', 'kind': 'public'}
        response = self.client.put(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        # test update diary (invalid title)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        data = {'title': '', 'kind': 'public'}
        response = self.client.put(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        # test update diary (invalid kind)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        data = {'title': 'diary 1 user 1 updated', 'kind': ''}
        response = self.client.put(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_delete_diary_detail(self):
        # test delete diary (with permissions) (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        data = {'title': 'diary 1 user 1 updated', 'kind': 'public', 'user': self.test_user1.id}
        response = self.client.delete(url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_error_delete_diary_detail(self):
        # test delete diary (non auth)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test1.id})
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test delete diary (without permissions) (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': self.diary_test3.id})
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'У вас недостаточно прав для выполнения данного действия.')
        self.client.logout()
        # test delete diary (invalid pk)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('diary-detail', kwargs = {'pk': 0})
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
