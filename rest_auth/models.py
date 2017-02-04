from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class PasswordRecovery(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255)

    def generate_token(self):
        token = get_random_string(length=6)
        self.token = make_password(token)
        self.save()
        return token

    def match(self, token):
        return check_password(token, self.token)
