from django.test import TestCase
from django.contrib.auth import get_user_model
from . import models


class TestPasswordRecovery(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('allo', 'allo@allo.com', 'allo')
        self.pr = models.PasswordRecovery(user=self.user)
        self.pr.save()

    def test_test_token(self):
        token = self.pr.generate_token()
        self.assertTrue(self.pr.match(token))
