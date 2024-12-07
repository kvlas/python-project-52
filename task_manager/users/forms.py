from django import forms
from task_manager.users.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name']




