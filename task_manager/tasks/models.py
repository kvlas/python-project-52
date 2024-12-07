from django.db import models
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 default='', related_name='executors')
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False, related_name='authors')


    def __str__(self):
        """Represent model object."""
        return self.name