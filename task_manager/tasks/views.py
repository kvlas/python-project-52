from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, \
    UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import UserLoginRequiredMixin, DeleteProtectionMixin

from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.labels.models import Label
from task_manager.tasks.filters import TaskFilter


class TaskListView(UserLoginRequiredMixin, FilterView):

    template_name = 'tasks/index.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }

class TaskDetailView(UserLoginRequiredMixin,
                     SuccessMessageMixin, DetailView):
    model = Task
    template_name = "tasks/task.html"
    context_object_name = "task"
    labels = Label.objects.all()
    extra_context = {'title': _('Task view'),
                     'btn_update': _('Update'),
                     'btn_delete': _('Delete'),
                     'labels': labels
                     }

class TaskCreateView(UserLoginRequiredMixin,
                     SuccessMessageMixin, CreateView):

    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    labels = Label.objects.all()
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')
    extra_context = {
        'title': _('Create Task'),
        'button_text': _('Create'),
        'labels': labels
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TaskUpdateView(UserLoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):

    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    labels = Label.objects.all()
    success_url = reverse_lazy('tasks')
    success_message = _('Task updated')
    extra_context = {
        'title': _('Update Task'),
        'button_text': _('Update'),
        'labels': labels
    }


class TaskDeleteView(UserLoginRequiredMixin, DeleteProtectionMixin,
                     SuccessMessageMixin, DeleteView):

    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task deleted')
    protected_message = _('You cannot delete task while it is in use')
    protected_url = reverse_lazy('tasks')
    extra_context = {
        'title': _('Delete Task'),
        'button_text': _('Yes, delete'),
    }
