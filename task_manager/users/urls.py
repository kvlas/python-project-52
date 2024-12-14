from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('<int:pk>/', views.UserView.as_view(), name='detail_user'),
    path('create/', views.UserCreateView.as_view(), name='create_user'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update_user'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete_user'),

]
