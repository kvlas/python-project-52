from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False,
                            verbose_name=_('Name'))
    description = models.TextField(blank=True,
                                   verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Creation date'))
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 default='', related_name="task_executor",
                                 verbose_name=_('Executor'))
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False, related_name="task_author",
                               verbose_name=_('Author'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               blank=False, related_name='task_statuses',
                               verbose_name=_('Status'))
    labels = models.ManyToManyField(Label, through='Connection',
                                    through_fields=('task', 'label'),
                                    blank=True, related_name='task_labels',
                                    verbose_name=_('Labels'))


    def __str__(self):
        """Represent model object."""
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

class Connection(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
