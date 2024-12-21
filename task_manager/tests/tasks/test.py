from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TestTask(TestCase):

    fixtures = ['labels.json', 'users.json', 'tasks.json', 'statuses.json']

    def test_create_logout(self):
        response = self.client.get(reverse_lazy('create_task'))
        self.assertEqual(response.status_code, 302)

    def test_create_task(self):
        user = User.objects.get(pk=1)
        status = Status.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 2)
        response = self.client.post(
            reverse_lazy('create_task'),
            {'name': 'task',
             'author': user.id,
             'status': status.id
             }
        )
        task = Task.objects.get(pk=3)
        self.assertEqual(Task.objects.all().count(), 3)
        self.assertEqual(task.__str__(), task.name)

    def test_update_logout(self):
        response = self.client.get(reverse_lazy('update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_task_update(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        status = Status.objects.all().first()
        self.client.force_login(user=user1)
        response = self.client.get(reverse_lazy('update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        new_task = {
            'name': 'task',
            'status': status.id,
            'executor': user2.id,
        }
        response = self.client.post(
            reverse_lazy('update_task', kwargs={'pk': 1}), new_task)
        status = Task.objects.get(pk=1)
        self.assertEqual(status.name, 'task')

    def test_delete_logout(self):
        response = self.client.get(reverse_lazy('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_delete_task(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('delete_task', kwargs={'pk': 1})
        )
        self.assertEqual(Task.objects.all().count(), 1)

    def test_delete_with_conn(self):
        task = Task.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertEqual(Task.objects.all().count(), 2)
        self.client.force_login(user=user)
        self.client.get(reverse_lazy('delete_task',
                        kwargs={'pk': task.id}))
        self.assertEqual(Task.objects.all().count(), 2)

    def test_list_logout(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 302)

    def test_list_login(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_filter_tasks(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse_lazy('tasks'),
            {'executor': 1}
        )

        self.assertEqual(response.context['tasks'].count(), 1)


class TaskSettings(TestCase):
    fixtures = ['tasks.json', 'labels.json', 'statuses.json', 'users.json']

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.get(username='test_user1')
        self.client.force_login(self.user)

        self.status = Status.objects.get(name='New status1')
        self.label = Label.objects.get(name='New label1')
        self.task = Task.objects.get(name='New Task1')

        self.urls = {
            'list': reverse('tasks'),
            'create': reverse('create_task'),
            'detail': lambda pk: reverse('task', args=[pk]),
            'update': lambda pk: reverse('update_task', args=[pk]),
            'delete': lambda pk: reverse('delete_task', args=[pk]),
        }


class TestTaskFilter(TaskSettings):
    def test_filter_by_executor(self):
        filter = TaskFilter(data={'executor': self.user.id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 2)
        self.assertEqual(filtered_tasks[0].name, 'New Task1')
        self.assertEqual(filtered_tasks[1].name, 'New Task3')

    def test_filter_by_label(self):
        filter = TaskFilter(data={
            'label': self.task.labels.first().id
        }, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 2)
        self.assertEqual(filtered_tasks[0].name, 'New Task1')
        self.assertEqual(filtered_tasks[1].name, 'New Task2')

    def test_filter_by_status(self):
        filter = TaskFilter(data={'status': self.status.id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 1)

    def test_filter_self_tasks(self):
        response = self.client.get(self.urls['list'], {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Task1')
        self.assertNotContains(response, 'New Task3')
