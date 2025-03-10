
from django.urls import path
from .views import get_page, del_task, complete_task, history_of_tasks, edit_task, del_from_history, restore_todo, edit_in_history

urlpatterns = [
    path('', get_page, name = 'main_page'),
    path('delete/<int:id>', del_task, name='delete_todo'),
    path('completed/<int:id>', complete_task, name='completed_task'),
    path('history/', history_of_tasks, name = 'history'),
    path('edit/<int:id>/', edit_task, name='edit_todo'),
    path('delete_history/<int:id>/', del_from_history, name = 'delete_history'),
    path('restore_todo/<int:id>/', restore_todo, name = 'restore_todo'),
    path('edit_in_history/<int:id>/', edit_in_history, name='edit_history'),
    ]
