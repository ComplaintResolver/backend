from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from root import models


class TestComplaintViewSet(APITestCase):

    def setUp(self):
        self.complainant = models.Complainant(account_type='twitter',
                                              account_handle='someone')
        self.complainant.save()
        self.complaint = models.Complaint(s_id='123',
                                          text="abcdcdcdcd",
                                          complainant=self.complainant)
        self.complaint.save()
        self.supervisor = models.Supervisor.objects.create_user(
            'beatles', 'beatles@beatles.com', 'beatles')
        self.client.force_authenticate(user=self.supervisor)

    def test_get_complaint_list(self):
        url = reverse('complaint-list')

        response = self.client.get(url)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['s_id'], '123')

    def test_get_complaint(self):
        url = reverse('complaint-detail', kwargs={'pk': 'some_random_id'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('complaint-detail', kwargs={'pk': self.complaint.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['s_id'], '123')

    def test_update_complaint(self):
        url = reverse('complaint-detail', kwargs={'pk': 123})
        response = self.client.patch(url, data={'status': 'resolved'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('complaint-detail', kwargs={'pk': self.complaint.id})
        response = self.client.patch(url, data={'status': 'something_something'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('complaint-detail', kwargs={'pk': self.complaint.id})
        response = self.client.patch(url, data={'status': 'resolved'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'resolved')


class TestCommentViewSet(APITestCase):

    def setUp(self):
        self.complainant = models.Complainant(account_type='twitter',
                                              account_handle='someone')
        self.complainant.save()
        self.complaint = models.Complaint(s_id='123',
                                          text="abcdcdcdcd",
                                          complainant=self.complainant)
        self.complaint.save()

        self.supervisor = models.Supervisor.objects.create_user(
            'beatles', 'beatles@beatles.com', 'beatles')
        self.client.force_authenticate(user=self.supervisor)

        self.comment = models.Comment(
            text="HAHAHAHA", supervisor=self.supervisor, s_id='12345', complaint=self.complaint)
        self.comment.save()

    def test_get_comment_list(self):
        url = reverse('complaint-comment-list', kwargs={'complaint_pk': self.complaint.id})
        response = self.client.get(url)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['s_id'], self.comment.s_id)

        url = reverse('complaint-comment-list', kwargs={'complaint_pk': 'some_random_pk'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self):
        url = reverse('complaint-comment-list', kwargs={'complaint_pk': self.complaint.id})
        response = self.client.post(url, data={'text': 'Hey! how are you?!!'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data={'text': 'This is my second comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
