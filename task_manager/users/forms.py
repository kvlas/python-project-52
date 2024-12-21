from django import forms
from task_manager.users.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150, required=True, label=_("First name")
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last name")
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_("Username"),
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2'
                  )


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=150, required=True, label=_("First name")
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last name")
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_("Username"),
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )
    password = None
    password_form = None

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username',)

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        self.password_form = SetPasswordForm(user)
        super().__init__(*args, **kwargs)
        
        # Добавляем поля SetPasswordForm
        self.fields.update(self.password_form.fields)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

    def clean(self):
        cleaned_data = super().clean()
        password_cleaned_data = self.password_form.clean()
        cleaned_data.update(password_cleaned_data)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        self.password_form.save()

        if commit:
            user.save()

        return user
