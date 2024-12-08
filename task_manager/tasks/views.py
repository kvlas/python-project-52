import django_filters
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'author', 'date_created'] 

class IndexView(View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        return render(request, 'tasks/index.html', context={
            'tasks': tasks, 'filter': task_filter
            })


class TaskView(View):

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['id'])
        return render(request, 'tasks/task.html', context={
            'task': task,
        })
    

class TaskCreateView(View):

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')

        return render(request, 'tasks/create.html', {'form': form})


class TaskUpdateView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        return render(request, 'tasks/update.html', {
            'form': form,
            'task_id': task_id
            }
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')

        return render(request, 'tasks/update.html', {
            'form': form,
            'task_id': task_id
            }
        )

class TaskDeleteView(View):

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
        return redirect('tasks')