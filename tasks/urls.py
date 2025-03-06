
from django.urls import path
from .views import get_page, del_task, complete_task

urlpatterns = [
    path('', get_page),
    path('delete/<int:id>', del_task, name='delete_todo'),
    path('completed/<int:id>', complete_task, name='completed_task')
]