from django.urls import path
from . import views

urlpatterns = [
    path('ola/', views.helloworld),
    path('', views.taskList, name='task-list'),
    path('nome/<str:name>', views.yourName, name='your-name'),
]
