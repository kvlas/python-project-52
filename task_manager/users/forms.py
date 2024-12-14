from django import forms
from task_manager.users.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label=_("First name"))
    last_name = forms.CharField(max_length=150, required=True, label=_("Last name"))


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
