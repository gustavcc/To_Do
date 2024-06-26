from django.urls import path
from . import views

urlpatterns = [
    path('', views.taskList, name='Task List'),
    path('task/<int:id>', views.taskView, name='Task View'),
    path('edit/<int:id>', views.taskEdit, name='Task Edit'),
    path('delete/<int:id>', views.taskDelete, name='Task Delete'),
    path('newtask/', views.newTask, name='New Task'),
]