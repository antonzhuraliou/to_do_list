from datetime import datetime, date
import calendar
from typing import Any

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Task, CompletedTask
from .forms import TodoForm, EditForm


def get_main_page(request):
    all_tasks = Task.objects.all()
    count_tasks = all_tasks.count()
    form = TodoForm()

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Task.objects.create(description = form.cleaned_data['add'])
            return HttpResponseRedirect('/')

    return render(request, 'tasks/cur_tasks.html', context = {'all_tasks': all_tasks, 'form': form, 'count_tasks': count_tasks})


def complete_task(request, id):
    task_to_delete = Task.objects.get(id=id)
    CompletedTask.objects.create(description = task_to_delete.description, created_at = datetime.now())
    task_to_delete.delete()
    return HttpResponseRedirect('/')


def delete_task(request, id):
    task_to_delete = Task.objects.get(id = id)
    task_to_delete.delete()
    return HttpResponseRedirect('/')


def edit_task(request, id):
    current_task = Task.objects.get(id = id)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form})


def task_history(request):
    all_tasks = CompletedTask.objects.all()
    distinct_dates = CompletedTask.objects.values('created_at').distinct().order_by('-created_at', )
    return render(request, 'tasks/history_page.html', context={'all_tasks': all_tasks, 'date': distinct_dates})


def delete_task_from_history(request, id):
    task_to_delete = CompletedTask.objects.get(id = id)
    task_to_delete.delete()
    return HttpResponseRedirect('/history')


def restore_task_from_history(request, id):
    task_to_restore = CompletedTask.objects.get(id=id)
    Task.objects.create(description = task_to_restore.description)
    task_to_restore.delete()
    return HttpResponseRedirect('/history')


def edit_task_in_history(request, id):
    current_task = CompletedTask.objects.get(id = id)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/history')

    else:
        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form})


def get_calendar(request):
    # Получаем количество дней в текущем месяце и передаем в контекст
    # Получаем цифровое значение первого дня в месяце для правильной генерации расположения календаря
    today_date = date.today()
    first_day_number, days_in_month = calendar.monthrange(today_date.year, today_date.month)
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days})