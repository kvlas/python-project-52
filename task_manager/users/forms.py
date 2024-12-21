from django import forms
from task_manager.users.models import User
from django.contrib.auth.forms import UserCreationForm
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


class UserUpdateForm(forms.ModelForm):
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
    new_password1 = forms.CharField(
        label=_("New password"),
        help_text=_("Your password must contain at least 3 characters."),
        widget=forms.PasswordInput,
        required=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        help_text=_("To confirm, please enter your password again."),
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_("The two password fields must match."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user
