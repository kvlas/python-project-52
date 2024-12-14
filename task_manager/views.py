from django.shortcuts import render, redirect
from django.contrib import messages
from task_manager.users.forms import UserForm


def index( request):
    return render(request, 'index.html')

def about( request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Вы успешно зарегистрировались!'))
            return redirect('login')  # Redirect to a login page or wherever you prefer
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})
