from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.http import HttpResponseRedirect
from tasks.forms import TodoForm, EditForm
from tasks.models import Task, CompletedTask

def get_calendar(request):
    # Получаем количество дней в текущем месяце и передаем в контекст
    # Получаем цифровое значение первого дня в месяце для правильной генерации расположения календаря
    today_date = date.today()
    first_day_number, days_in_month = calendar.monthrange(today_date.year, today_date.month)
    actual_month = calendar.month_name[today_date.month]
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'calendar_tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days,
                                                                  'today_year': today_date, 'actual_month': actual_month, 'today_compare': date.today()})

def get_priv_or_next_calendar(request, month, year, sign):
    if sign == '+':
        current_month_date = date(year, month, 1) + relativedelta(months=1)
    else:
        current_month_date = date(year, month, 1) - relativedelta(months=1)
    first_day_number, days_in_month = calendar.monthrange(current_month_date.year, current_month_date.month)
    actual_month = calendar.month_name[current_month_date.month]
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'calendar_tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days,
                                                                  'today_year': current_month_date, 'actual_month': actual_month, 'today_compare': date.today()})

def calendar_task(request, day, month, year):
    all_tasks = Task.objects.filter(created_at__date = date(year, month, day))
    actual_month = calendar.month_name[month]
    date_to_add = (year, actual_month, day, month)
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Task.objects.create(description=form.cleaned_data['description'], created_at = date(year, month, day))
            return HttpResponseRedirect(f'/calendar/task_for_day/{day}/{month}/{year}/')

    return render(request, 'calendar_tasks/day_task_page.html', context = {'form': form, 'date_to_add':date_to_add, 'all_tasks': all_tasks})


def get_completed_tasks(request, day, month, year):
    actual_month = calendar.month_name[month]
    date_to_add = (year, actual_month, day, month)
    completed_tasks = CompletedTask.objects.filter(created_at= date(year, month, day))
    return render(request,  'calendar_tasks/completed_task.html', context = {'completed_tasks': completed_tasks, 'date_to_add': date_to_add})


def delete_task_from_day(request, id, day, month, year):
    today_date = date.today()
    if  day > today_date.day and month == today_date.month  or month > today_date.month or year > today_date.year:
        task_to_delete = Task.objects.get(id=id)
        task_to_delete.delete()
        return HttpResponseRedirect(f'/calendar/task_for_day/{day}/{month}/{year}/')
    else:
        task_to_delete = CompletedTask.objects.get(id=id)
        task_to_delete.delete()
        return HttpResponseRedirect(f'/calendar/task_for_day_past/{day}/{month}/{year}/')

def edit_task_calendar(request, id, day, month, year):
    today_date = date.today()
    which_edit = 'Calendar'
    if day > today_date.day and month == today_date.month or month > today_date.month or year > today_date.year:
        current_task = Task.objects.get(id=id)
        if request.method == 'POST':
            form = EditForm(request.POST, instance=current_task)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/calendar/task_for_day/{day}/{month}/{year}/')
        else:
            form = EditForm(instance=current_task)
    else:
        current_task = CompletedTask.objects.get(id=id)
        if request.method == 'POST':
            form = EditForm(request.POST, instance=current_task)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/calendar/task_for_day_past/{day}/{month}/{year}/')

        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'which_edit': which_edit})


def show_welcome_page(request):
    return render(request, 'calendar_tasks/welcome_page.html')