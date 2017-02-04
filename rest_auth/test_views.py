from django.urls import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import get_user_model, authenticate

from . import views
from . import models


class AuthTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('beatles',
                                                         'beatles@beatles.com',
                                                         'beatlesisgreat')

    def test_change_password(self):
        url = reverse(views.change_password)
        self.client.force_authenticate(user=self.user)

        data = {'old_password': 'india', 'new_password': 'indiatoo'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'old_password': ['Invalid credentials']})
        self.assertIs(authenticate(username='beatles', password='indiatoo'), None)

        data = {'old_password': 'beatlesisgreat', 'new_password': 'indiatoo'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(authenticate(username='beatles', password='indiatoo'), None)

    def test_forgot_password(self):
        url = reverse(views.forgot_password)

        data = {'username': 'guysensei'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'username': 'beatles'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertIsNot(self.user.passwordrecovery, None)
        self.assertEqual(len(mail.outbox), 1)
        _, token = str(mail.outbox[0].message()).rsplit(':', 1)
        token = token.strip()
        self.assertTrue(self.user.passwordrecovery.match(token))

        url = reverse(views.forgot_password_done)
        data = {'username': 'beatles', 'token': token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'username': 'guysensei', 'token': token, 'password': 'indiatoo'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'username': 'beatles', 'token': token, 'password': 'india'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'username': 'beatles', 'token': token, 'password': 'indiatoo'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()
