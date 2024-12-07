from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'statuses/index.html', context={
            'statuses': statuses,
        })


class StatusView(View):

    def get(self, request, *args, **kwargs):
        status = get_object_or_404(Status, id=kwargs['id'])
        return render(request, 'statuses/status.html', context={
            'status': status,
        })
    
class StatusCreateView(View):

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'statuses/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('statuses_index')

        return render(request, 'statuses/create.html', {'form': form})


class StatusUpdateView(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(instance=status)
        return render(request, 'statuses/update.html', {
            'form': form,
            'status_id': status_id
            }
        )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('statuses_index')

        return render(request, 'statuses/update.html', {
            'form': form,
            'status_id': status_id
            }
        )

class StatusDeleteView(View):

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        if status:
            status.delete()
        return redirect('statuses_index')