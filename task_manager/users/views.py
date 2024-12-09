from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
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
            return redirect('users')

        return render(request, 'users/create.html', {'form': form})


class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(request, 'users/update.html', {
            'form': form,
            'user_id': user_id
            }
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')

        return render(request, 'users/update.html', {
            'form': form,
            'user_id': user_id
            }
        )

class UserDeleteView(View):

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users')