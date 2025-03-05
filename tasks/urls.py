
from django.urls import path
from .views import get_page, del_page

urlpatterns = [
    path('', get_page),
    path('delete/<int:id>', del_page, name='delete_todo')
]