from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from task_manager.users.forms import UserForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users,
        })


class UserView(View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        return render(request, 'users/user.html', context={
            'user': user,
        })


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Пользователь успешно зарегистрирован'))
            return redirect('login')

        return render(request, 'users/create.html', {'form': form})
    

class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = UserForm(instance=user)
        return render(request, 'users/create.html', {'form': form, 'user': user})


    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('User details updated successfully'))
            return redirect('users')
        return render(request, 'users/create.html', {'form': form, 'user': user})
    
class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = UserForm(instance=user)
        return render(request, 'users/update.html', {'form': form, 'user': user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('User details updated successfully'))
            return redirect('users')
        return render(request, 'users/update.html', {'form': form, 'user': user})

class UserDeleteView(View):
  
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        return render(request, 'users/delete.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        try:
            user.delete()
            messages.success(request, _("User was successfully deleted."))
        except Exception as e:
            messages.error(request, _("An error occurred while deleting the user: ") + str(e))
        return redirect('users')