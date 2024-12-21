from django import forms
from task_manager.users.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username',)

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
    #         raise forms.ValidationError(_("A user with that username already exists."))
    #     return username

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")

    #     if password1 or password2:
    #         if password1 != password2:
    #             raise forms.ValidationError(_("The two password fields must match."))

    #     return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     new_password = self.cleaned_data.get("password1")

    #     if new_password:
    #         user.set_password(new_password)

    #     if commit:
    #         user.save()

    #     return user
