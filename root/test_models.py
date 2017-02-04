from django.test import TestCase
from django.core.exceptions import ValidationError
from . import models


class TestSupervisor(TestCase):

    def test_create_supervisor(self):
        s = models.Supervisor.objects.create_user('beatles',
                                                  'beatles@beatles.com',
                                                  'beatles')
        s.designation = 'Oyeeeeeee'
        s.save()


class TestComplainant(TestCase):

    def test_create_complainant(self):
        c1 = models.Complainant(account_type='twitter',
                                account_handle='india')
        c1.full_clean()
        c1.save()
        with self.assertRaises(ValidationError):
            c2 = models.Complainant(account_type='twir',
                                    account_handle='india')
            c2.full_clean()


class TestComplaint(TestCase):

    def setUp(self):
        self.complainant = models.Complainant(account_type='twitter',
                                              account_handle='india')
        self.complainant.save()

    def test_create_complaint(self):
        c = models.Complaint(s_id='123', text='India', complainant=self.complainant)
        c.full_clean()


class Comment(TestCase):

    def setUp(self):
        self.complainant = models.Complainant(account_type='twitter',
                                              account_handle='india')
        self.complainant.save()
        self.supervisor = models.Supervisor.objects.create_user('beatles',
                                                                'beatles@beatles.com',
                                                                'beatles')
        self.supervisor.save()
        self.complaint = models.Complaint(s_id='123', text='India', complainant=self.complainant)
        self.complaint.save()

    def test_create_comment(self):
        supervisor_c = models.Comment(supervisor=self.supervisor,
                                      complaint=self.complaint,
                                      s_id='12345E',
                                      text="somethin something")
        supervisor_c.full_clean()
        supervisor_c.save()

        complainant_c = models.Comment(complainant=self.complainant,
                                       complaint=self.complaint,
                                       s_id='12345E',
                                       text="somethin something")
        complainant_c.full_clean()
        complainant_c.save()
