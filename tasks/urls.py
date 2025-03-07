
from django.urls import path
from .views import get_page, del_task, complete_task, history_of_tasks, edit_task

urlpatterns = [
    path('', get_page),
    path('delete/<int:id>', del_task, name='delete_todo'),
    path('completed/<int:id>', complete_task, name='completed_task'),
    path('history/', history_of_tasks, name = 'history'),
    path('edit/<int:id>', edit_task, name='edit_todo')
]