from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta
from typing import Any

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Task, CompletedTask
from .forms import TodoForm, EditForm, SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

@login_required
def get_main_page(request):
    today_day = date.today().day # Используется для указания дня у иконки Календаря на главном меню
    today_date = date.today()

    user_id = request.user.id
    all_tasks = Task.objects.filter(created_at__date = today_date, user_id = user_id) # получаем все задания, у которых сегодняшняя дата
    count_tasks = all_tasks.count() # высчитываем количество задач для счетчика

    # Данный блок нужен для сохранения задач, которые не удалось выполнить в предыдущий день
    not_completed_tasks = Task.objects.filter(created_at__date__lt=today_date, user_id = user_id)  # Получаем задачи, которые не выполнены в предыдyщие дни
    # Проверяем есть ли такие задачи, если есть то добавляем их в выполненные, но со статусом False
    if not_completed_tasks:
        list_of_not_completed_tasks = [CompletedTask(description=task.description, created_at=task.created_at, is_completed= False, user_id = user_id) for task in not_completed_tasks]
        CompletedTask.objects.bulk_create(list_of_not_completed_tasks) # Сохраняем сразу все задачи в бд
        not_completed_tasks.delete() # Удаляем их из таблицы с задачи до выполнения

    # Форма для создания задач для выполнения и после создания задачи перенаправляем на корневую папку
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Task.objects.create(description = form.cleaned_data['description'], created_at = date(today_date.year, today_date.month, today_date.day), user_id = user_id)
            return redirect('tasks:main_page')

    return render(request, 'tasks/cur_tasks.html', context = {'all_tasks': all_tasks, 'form': form, 'count_tasks': count_tasks, 'today_day': today_day})

@login_required
def complete_task(request, id):
    user_id = request.user.id
    task_to_delete = Task.objects.get(id=id, )
    CompletedTask.objects.create(description = task_to_delete.description, created_at = datetime.now(), user_id = user_id)
    task_to_delete.delete()
    return redirect('tasks:main_page')

@login_required
def delete_task(request, id):
    user_id = request.user.id
    task_to_delete = Task.objects.get(id = id, user_id = user_id)
    task_to_delete.delete()
    return redirect('tasks:main_page')

@login_required
def edit_task(request, id):
    user_id = request.user.id
    current_task = Task.objects.get(id = id, user_id = user_id)
    which_edit = 'Task'
    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()

            return redirect('tasks:main_page')
    else:
        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'which_edit': which_edit})

@login_required
def task_history(request):
    user_id = request.user.id
    all_tasks = CompletedTask.objects.filter(is_completed=True, user_id = user_id)
    form = SearchForm()
    distinct_dates = CompletedTask.objects.filter(is_completed=True, user_id = user_id).values('created_at').distinct().order_by(
        '-created_at', )
    return render(request, 'tasks/history_page.html',
                  context={'all_tasks': all_tasks, 'date': distinct_dates, 'form': form})

@login_required
@require_GET
def search_history(request):
    user_id = request.user.id
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        all_tasks = CompletedTask.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(
                similarity__gt=0.2, user_id = user_id)
        distinct_dates = all_tasks.filter(is_completed=True, user_id=user_id).values('created_at').distinct().order_by(
                '-created_at', )
    else:
        all_tasks = None
        distinct_dates = None
        query = None
    return render(request, 'tasks/search_history.html',
                  context={'all_tasks': all_tasks, 'date': distinct_dates, 'form': form, 'query': query})

@login_required
def delete_task_from_history(request, id, query):
    user_id = request.user.id
    task_to_delete = CompletedTask.objects.get(id = id, user_id=user_id)
    task_to_delete.delete()
    if query:
        url = reverse('tasks:search')
        return HttpResponseRedirect(f'{url}?query={query}')
    return HttpResponseRedirect('/history')

@login_required
def restore_task_from_history(request, id, query):
    user_id = request.user.id
    task_to_restore = CompletedTask.objects.get(id=id, user_id=user_id)
    Task.objects.create(description = task_to_restore.description, created_at = date.today(), user_id=user_id)
    task_to_restore.delete()
    if query:
        url = reverse('tasks:search')
        return HttpResponseRedirect(f'{url}?query={query}')
    return HttpResponseRedirect('/history')

@login_required
def edit_task_in_history(request, id, query):
    user_id = request.user.id
    current_task = CompletedTask.objects.get(id = id, user_id=user_id)
    which_edit = 'History_search' if query != '-' else 'History'
    if request.method == 'POST':
        form = EditForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            if query != '-':
                url = reverse('tasks:search')
                return HttpResponseRedirect(f'{url}?query={query}')

            return HttpResponseRedirect('/history')

    else:
        form = EditForm(instance=current_task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'which_edit': which_edit, 'query': query})
