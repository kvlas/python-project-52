from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 default='', related_name="task_executor")
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False, related_name="task_author")
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               blank=False, related_name='task_statuses')
    labels = models.ManyToManyField(Label, through='Connection',
                                    through_fields=('task', 'label'),
                                    blank=True, related_name='task_labels')


    def __str__(self):
        """Represent model object."""
        return self.name

class Connection(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)