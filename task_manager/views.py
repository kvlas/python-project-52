from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class UserLoginView(LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    success_message = _('You are logged in')
    extra_context = {
        'title': _('Login'),
        'button_text': _('Enter'),
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    success_message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)