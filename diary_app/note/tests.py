from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from account.models import User

from .models import Diary, Note


class NotesTests(APITestCase):
    def setUp(self):
        # urls
        self.url_list = reverse('note-list')

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

        # create fake diaries
        self.diary_test1 = Diary.objects.create(title = 'diary 1 user 1', kind = 'public', user = self.test_user1)
        self.diary_test2 = Diary.objects.create(title = 'diary 2 user 1', kind = 'public', user = self.test_user1)
        self.diary_test3 = Diary.objects.create(title = 'diary 1 user 2', kind = 'public', user = self.test_user2)
        self.diary_test4 = Diary.objects.create(title = 'diary 2 user 2', kind = 'public', user = self.test_user2)

        # create fake notes for diary
        self.note_test1 = Note.objects.create(content = 'note 1 diary 1', diary = self.diary_test1)
        self.note_test2 = Note.objects.create(content = 'note 2 diary 1', diary = self.diary_test2)
        self.note_test3 = Note.objects.create(content = 'note 3 diary 1', diary = self.diary_test3)
        self.note_test4 = Note.objects.create(content = 'note 4 diary 1', diary = self.diary_test4)
        self.note_test5 = Note.objects.create(content = 'note 1 diary 2', diary = self.diary_test1)
        self.note_test6 = Note.objects.create(content = 'note 2 diary 2', diary = self.diary_test2)
        self.note_test7 = Note.objects.create(content = 'note 3 diary 2', diary = self.diary_test3)
        self.note_test8 = Note.objects.create(content = 'note 4 diary 2', diary = self.diary_test4)


    def test_get_note_list(self):
        # test get note list (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 8)
        self.client.logout()

    def test_error_get_note_list(self):
        # test get note list (non auth)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')

    def test_post_note_list(self):
        # test create new note (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'content': 'new note', 'diary': self.diary_test1.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        # test create new note (repeat data)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'content': 'note', 'diary': self.diary_test1.id}
        response = self.client.post(self.url_list, data = data)
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_error_post_note_list(self):
        # test create new note (non auth)
        data = {'content': 'new note', 'diary': self.diary_test1.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test create new note (invalid diary id)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'content': 'new note', 'diary': 1000}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        # test create new note (invalid content)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'content': '', 'diary': self.diary_test1.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        # test create new note (invalid user)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        data = {'content': 'note', 'diary': self.diary_test3.id}
        response = self.client.post(self.url_list, data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_get_note_detail(self):
        # test get note detail (auth)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('note-detail', kwargs = {'pk': self.note_test1.id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_error_get_note_detail(self):
        # test get note detail (non auth)
        url_detail = reverse('note-detail', kwargs = {'pk': self.note_test1.id})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Учетные данные не были предоставлены.')
        # test get diary detail (invalid pk)
        self.client.login(email = 'user1@user.ru', password = 'user')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.test_user1_token.key)
        url_detail = reverse('note-detail', kwargs = {'pk': 0})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
