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
        self.password_form = SetPasswordForm(user, data=kwargs.get('data'))
        super().__init__(*args, **kwargs)
        
        # Hexlet tests
        if 'new_password1' in self.password_form.fields:
            self.password_form.fields['new_password1'].widget.attrs.update({'id': 'id_password1'})
        if 'new_password2' in self.password_form.fields:
            self.password_form.fields['new_password2'].widget.attrs.update({'id': 'id_password2'})
        if 'new_password1' in self.password_form.fields:
            self.password_form.fields['new_password1'].label = _("Password")
        if 'new_password2' in self.password_form.fields:
            self.password_form.fields['new_password2'].label = _("Confirm password")
    
        self.fields.update(self.password_form.fields)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username
   
    def clean(self):
        cleaned_data = super().clean()
        
        if self.password_form.is_valid():
            password_cleaned_data = self.password_form.cleaned_data
            cleaned_data.update(password_cleaned_data)            
        else:
            for field, errors in self.password_form.errors.items():
                for error in errors:
                    self.add_error(field, error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.password_form.is_valid():
            self.password_form.save()

        if commit:
            user.save()

        return user
