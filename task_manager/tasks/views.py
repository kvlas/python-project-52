from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, 'tasks/index.html', context={
            'tasks': tasks,
        })


class TaskView(View):

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['id'])
        return render(request, 'tasks/task.html', context={
            'task': task,
        })