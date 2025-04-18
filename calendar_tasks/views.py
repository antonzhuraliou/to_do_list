from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, reverse, redirect
from tasks.forms import TodoForm, EditForm
from tasks.models import Task, CompletedTask
from django.contrib.auth.decorators import login_required


@login_required
def get_calendar(request):
    # Получаем количество дней в текущем месяце и передаем в контекст
    # Получаем цифровое значение первого дня в месяце для правильной генерации расположения календаря
    today_date = date.today()
    first_day_number, days_in_month = calendar.monthrange(today_date.year, today_date.month)
    actual_month = calendar.month_name[today_date.month]
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'calendar_tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days,
                                                                  'today_year': today_date, 'actual_month': actual_month, 'today_compare': date.today()})


@login_required
def get_priv_or_next_calendar(request, month, year, sign = ''):
    if sign == '+':
        current_month_date = date(year, month, 1) + relativedelta(months=1)
    elif sign == '-':
        current_month_date = date(year, month, 1) - relativedelta(months=1)
    else:
        current_month_date = date(year, month, 1)
    first_day_number, days_in_month = calendar.monthrange(current_month_date.year, current_month_date.month)
    actual_month = calendar.month_name[current_month_date.month]
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render(request, 'calendar_tasks/calendar_page.html', context = {'days_in_month': days_in_month, 'empty_days': first_day_number, 'week_days':week_days,
                                                                  'today_year': current_month_date, 'actual_month': actual_month, 'today_compare': date.today()})


@login_required
def calendar_task(request, day, month, year):
    user_id = request.user.id
    all_tasks = Task.objects.filter(created_at__date = date(year, month, day), user_id=user_id)
    actual_month = calendar.month_name[month]
    date_to_add = (year, actual_month, day, month)
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Task.objects.create(description=form.cleaned_data['description'], created_at = date(year, month, day), user_id=user_id)
            return redirect(reverse('calendar_tasks:day_task', kwargs={'day':day,'month': month, 'year': year}))

    return render(request, 'calendar_tasks/day_task_page.html', context = {'form': form, 'date_to_add':date_to_add, 'all_tasks': all_tasks, 'month': month})


@login_required
def get_completed_tasks(request, day, month, year):
    user_id = request.user.id
    actual_month = calendar.month_name[month]
    date_to_add = (year, actual_month, day, month)
    completed_tasks = CompletedTask.objects.filter(created_at= date(year, month, day), user_id=user_id)
    return render(request,  'calendar_tasks/completed_task.html', context = {'completed_tasks': completed_tasks, 'date_to_add': date_to_add, 'month': month})


@login_required
def delete_task_from_day(request, id, day, month, year):
    today_date = date.today()
    user_id = request.user.id

    is_future_task = day > today_date.day and month == today_date.month  or month > today_date.month or year > today_date.year
    if is_future_task:
        task_model = Task
        redirect_url = reverse('calendar_tasks:day_task', kwargs={'day':day,'month': month, 'year': year})
    else:
        task_model = CompletedTask
        redirect_url = reverse('calendar_tasks:completed_task', kwargs={'day':day,'month': month, 'year': year})

    task_to_delete = task_model.objects.get(id=id, user_id=user_id)
    if request.method == 'POST':
        task_to_delete.delete()
        return redirect(redirect_url)

    url_page = 'calendar_tasks:day_task' if is_future_task else 'calendar_tasks:completed_task'
    context = {'url_page': url_page, 'query': '+', 'day':day,'month': month, 'year': year}

    return render(request, 'delete_with_confirm.html', context=context)


@login_required
def edit_task_calendar(request, id, day, month, year):
    today_date = date.today()
    user_id = request.user.id

    is_future_task = day > today_date.day and month == today_date.month or month > today_date.month or year > today_date.year
    if is_future_task:
        which_edit = 'Calendar_last'
        task_model = Task
        redirect_url = reverse('calendar_tasks:day_task', kwargs={'day':day,'month': month, 'year': year})
    else:
        which_edit = 'Calendar_future'
        task_model = CompletedTask
        redirect_url = reverse('calendar_tasks:completed_task', kwargs={'day':day,'month': month, 'year': year})

    current_task = task_model.objects.get(id=id, user_id=user_id)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
         form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'which_edit': which_edit, 'date': date(year, month, day)})


