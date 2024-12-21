from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import UserLoginRequiredMixin, DeleteProtectionMixin
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm


class LabelListView(UserLoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'
    extra_context = {
        'title': _('Labels')
    }


class LabelCreateView(UserLoginRequiredMixin,
                      SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(UserLoginRequiredMixin,
                      SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('Label updated')
    extra_context = {
        'title': _('Update Label'),
        'button_text': _('Update'),
    }


class LabelDeleteView(UserLoginRequiredMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):
    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label deleted')
    protected_message = _('You cannot delete label while it is in use')
    protected_url = reverse_lazy('labels')
    extra_context = {
        'title': _('Delete Label'),
        'button_text': _('Yes, delete'),
    }
