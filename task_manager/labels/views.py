from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        task_filter = None
        return render(request, 'labels/index.html', context={
            'labels': labels,
            'filter': task_filter
        })


class LabelView(View):

    def get(self, request, *args, **kwargs):
        label = get_object_or_404(Label, id=kwargs['id'])
        return render(request, 'labels/label.html', context={
            'label': label,
        })
    
class LabelCreateView(View):

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, 'labels/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('labels')

        return render(request, 'labels/create.html', {'form': form})


class LabelUpdateView(View):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(instance=label)
        return render(request, 'labels/update.html', {
            'form': form,
            'label_id': label_id
            }
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect('labels')

        return render(request, 'labels/update.html', {
            'form': form,
            'label_id': label_id
            }
        )

class LabelDeleteView(View):

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        if label:
            label.delete()
        return redirect('labels')