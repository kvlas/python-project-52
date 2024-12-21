from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class TestStatus(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.get(username='test_user1')
        self.client.force_login(self.user)

        self.status = Status.objects.get(name='New status1')

        self.urls = {
            'list': reverse('statuses'),
            'create': reverse('create_status'),
            'update': lambda pk: reverse('update_status', args=[pk]),
            'delete': lambda pk: reverse('delete_status', args=[pk]),
        }

    def test_status_list(self):
        response = self.client.get(self.urls['list'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New status1')

    def test_create_status(self):
        response = self.client.post(
            self.urls['create'],
            {'name': 'test status'}
        )
        self.assertRedirects(response, self.urls['list'], 302)
        self.assertEqual(Status.objects.count(), 3)

    def test_update_status(self):
        response = self.client.get(self.urls['update'](self.status.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_form.html')

        response = self.client.post(
            self.urls['update'](self.status.pk),
            {'name': 'Updated Name'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Name')

    def test_delete_status(self):
        response = self.client.post(self.urls['delete'](self.status.pk))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 1)
