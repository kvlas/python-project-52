from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='labels'),
    path('<int:pk>/', views.LabelView.as_view(), name='detail_label'),
    path('create/', views.LabelCreateView.as_view(), name='create_label'),
    path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='update_label'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='delete_label'),
]
