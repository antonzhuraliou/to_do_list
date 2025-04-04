from django.urls import path
from calendar_tasks import views

app_name = 'calendar_tasks'

urlpatterns = [
    path('get_calendar/', views.get_calendar, name='calendar'),
    path('task_for_day/<int:day>/<int:month>/<int:year>/', views.calendar_task, name = 'day_task'),
    path('task_for_day_past/<int:day>/<int:month>/<int:year>/', views.get_completed_tasks, name = 'completed_task'),
    path('change_month/<int:month>/<int:year>/<str:sign>', views.get_priv_or_next_calendar, name='change_month'),
    path('delete_task_for_day/<int:id>/<int:day>/<int:month>/<int:year>/', views.delete_task_from_day, name='today_delete'),
    path('edit_task_for_day/<int:id>/<int:day>/<int:month>/<int:year>/', views.edit_task_calendar, name = 'today_edit'),
]