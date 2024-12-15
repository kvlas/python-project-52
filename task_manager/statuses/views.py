from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import UserLoginRequiredMixin, DeleteProtectionMixin
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusListView(UserLoginRequiredMixin, ListView):

    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses')
    }


class StatusCreateView(UserLoginRequiredMixin,
                       SuccessMessageMixin, CreateView):

    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(UserLoginRequiredMixin,
                       SuccessMessageMixin, UpdateView):

    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status updated')
    extra_context = {
        'title': _('Update status'),
        'button_text': _('Update'),
    }


class StatusDeleteView(UserLoginRequiredMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):

    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status deleted')
    protected_message = _('You cannot delete staus while it is in use')
    protected_url = reverse_lazy('statuses')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
