from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta
from typing import Any

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Task, CompletedTask
from .forms import TodoForm, EditForm


def get_main_page(request):
    today_day = date.today().day # Используется для указания дня у иконки Календаря на главном меню
    today_date = date.today()

    all_tasks = Task.objects.filter(created_at__date = today_date) # получаем все задания, у которых сегодняшняя дата
    count_tasks = all_tasks.count() # высчитываем количество задач для счетчика

    # Данный блок нужен для сохранения задач, которые не удалось выполнить в предыдущий день
    not_completed_tasks = Task.objects.filter(created_at__date__lt=today_date)  # Получаем задачи, которые не выполнены в предыдyщие дни
    # Проверяем есть ли такие задачи, если есть то добавляем их в выполненные, но со статусом False
    if not_completed_tasks:
        list_of_not_completed_tasks = [CompletedTask(description=task.description, created_at=task.created_at, is_completed= False) for task in not_completed_tasks]
        CompletedTask.objects.bulk_create(list_of_not_completed_tasks) # Сохраняем сразу все задачи в бд
        not_completed_tasks.delete() # Удаляем их из таблицы с задачи до выполнения

    # Форма для создания задач для выполнения и после создания задачи перенаправляем на корневую папку
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Task.objects.create(description = form.cleaned_data['description'], created_at = date(today_date.year, today_date.month, today_date.day))
            return HttpResponseRedirect('/')

    return render(request, 'tasks/cur_tasks.html', context = {'all_tasks': all_tasks, 'form': form, 'count_tasks': count_tasks, 'today_day': today_day})


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
    which_edit = 'Task'
    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'which_edit': which_edit})


def task_history(request):
    all_tasks = CompletedTask.objects.filter(is_completed=True)
    distinct_dates = CompletedTask.objects.filter(is_completed=True).values('created_at').distinct().order_by('-created_at', )

    return render(request, 'tasks/history_page.html', context={'all_tasks': all_tasks, 'date': distinct_dates})


def delete_task_from_history(request, id):
    task_to_delete = CompletedTask.objects.get(id = id)
    task_to_delete.delete()
    return HttpResponseRedirect('/history')


def restore_task_from_history(request, id):
    task_to_restore = CompletedTask.objects.get(id=id)
    Task.objects.create(description = task_to_restore.description, created_at = date.today())
    task_to_restore.delete()
    return HttpResponseRedirect('/history')


def edit_task_in_history(request, id):
    current_task = CompletedTask.objects.get(id = id)
    which_edit = 'History'
    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/history')

    else:
        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'which_edit': which_edit})


def get_calendar(request):
    # Получаем количество дней в текущем месяце и передаем в контекст
    # Получаем цифровое значение первого дня в месяце для правильной генерации расположения календаря
    today_date = date.today()
    first_day_number, days_in_month = calendar.monthrange(today_date.year, today_date.month)
    actual_month = calendar.month_name[today_date.month]
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days,
                                                                  'today_year': today_date, 'actual_month': actual_month})

def get_priv_or_next_calendar(request, month, year, sign):
    if sign == '+':
        current_month_date = date(year, month, 1) + relativedelta(months=1)
    else:
        current_month_date = date(year, month, 1) - relativedelta(months=1)
    first_day_number, days_in_month = calendar.monthrange(current_month_date.year, current_month_date.month)
    actual_month = calendar.month_name[current_month_date.month]
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days,
                                                                  'today_year': current_month_date, 'actual_month': actual_month})

def calendar_task(request, day, month, year):
    all_tasks = Task.objects.filter(created_at__date = date(year, month, day))
    actual_month = calendar.month_name[month]
    date_to_add = (year, actual_month, day)
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Task.objects.create(description=form.cleaned_data['description'], created_at = date(year, month, day))
            return HttpResponseRedirect(f'/task_for_day/{day}/{month}/{year}/')

    return render(request, 'tasks/day_task_page.html', context = {'form': form, 'date_to_add':date_to_add, 'all_tasks': all_tasks})


def get_completed_tasks(request, day, month, year):
    actual_month = calendar.month_name[month]
    date_to_add = (year, actual_month, day)
    completed_tasks = CompletedTask.objects.filter(created_at= date(year, month, day))
    return render(request,  'tasks/completed_task.html', context = {'completed_tasks': completed_tasks, 'date_to_add': date_to_add})