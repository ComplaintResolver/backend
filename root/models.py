from django.db import models
from django.contrib.auth.models import AbstractUser


class Supervisor(AbstractUser):
    designation = models.CharField(max_length=255, default='admin')


class Complaint(models.Model):
    ALL_STATUS = (
        ('waiting', 'waiting'),
        ('resolved', 'resolved'),
        ('rejected', 'rejected')
    )
    s_id = models.TextField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ALL_STATUS,
                              max_length=255,
                              default='waiting',
                              blank=True)
    complainant = models.ForeignKey('Complainant', on_delete=models.CASCADE)


class Complainant(models.Model):
    ACCOUNT_TYPES = (
        ('twitter', 'twitter'),
    )
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=255)
    account_handle = models.CharField(max_length=255)


class Comment(models.Model):
    supervisor = models.ForeignKey('Supervisor',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)

    complainant = models.ForeignKey('Complainant',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
    s_id = models.TextField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    complaint = models.ForeignKey(Complaint)
    next_comment = models.OneToOneField('Comment',
                                        null=True,
                                        on_delete=models.SET_NULL,
                                        blank=True)
