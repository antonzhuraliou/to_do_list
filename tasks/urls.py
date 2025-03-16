
from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.get_main_page, name = 'main_page'),
    path('delete/<int:id>', views.delete_task, name='delete_todo'),
    path('complete/<int:id>', views.complete_task, name='complete_todo'),
    path('edit/<int:id>/', views.edit_task, name='edit_todo'),
    path('history/', views.task_history, name = 'history'),
    path('delete_task_from_history/<int:id>/', views.delete_task_from_history, name = 'history_delete'),
    path('restore_task_from_history/<int:id>/', views.restore_task_from_history, name = 'history_restore'),
    path('edit_task_in_history/<int:id>/', views.edit_task_in_history, name='history_edit'),
    path('get_calendar/', views.get_calendar, name='calendar'),
    path('task_for_day/<int:day>/<int:month>/<int:year>/', views.calendar_task, name = 'day_task'),
    path('task_for_day_past/<int:day>/<int:month>/<int:year>/', views.get_completed_tasks, name = 'completed_task'),
    path('change_month/<int:month>/<int:year>/<str:sign>', views.get_priv_or_next_calendar, name='change_month'),
    ]
