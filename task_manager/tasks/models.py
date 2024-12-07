from django.db import models
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False,
                            verbose_name=_('Name'))
    description = models.TextField(blank=True,
                                   verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Creation date'))
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 default='', related_name='executors',
                                 verbose_name=_('Executor'))
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False, related_name='authors',
                               verbose_name=_('Author'))


    def __str__(self):
        """Represent model object."""
        return self.name