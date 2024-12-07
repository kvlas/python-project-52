from django.contrib import admin
from task_manager.users.models import User
from task_manager.tasks.models import Task

admin.site.register(User)
admin.site.register(Task)