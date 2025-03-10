from django.shortcuts import render
from .models import Task, CompletedTask
from .forms import TodoForm
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.views.generic import UpdateView
from .forms import EditForm
import typing

def get_page(request):
    tasks = Task.objects.all()
    form = TodoForm()
    count_tasks = Task.objects.all().count()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            new_tasks = Task.objects.create(description = form.cleaned_data['add'])
            count_tasks += 1
            return HttpResponseRedirect('/')
    return render(request, 'tasks/cur_tasks.html', context = {'tasks': tasks, 'form': form, 'count': count_tasks})

def del_task(request, id):
    delete_task = Task.objects.get(id = id)
    delete_task.delete()
    return HttpResponseRedirect('/')

def complete_task(request, id):
    delete_task = Task.objects.get(id=id)
    completed_task = CompletedTask(description = delete_task.description, created_at = datetime.now())
    delete_task.delete()
    completed_task.save()
    return HttpResponseRedirect('/')


def history_of_tasks(request):
    all_tasks = CompletedTask.objects.all()
    create_tasks = CompletedTask.objects.values('created_at').distinct().order_by('-created_at', )
    return render(request, 'tasks/history_page.html', context={'all_tasks': all_tasks, 'date': create_tasks})

def edit_task(request, id):
    cur_task = Task.objects.get(id = id)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=cur_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EditForm(instance=cur_task)
    return render(request, 'tasks/edit_task.html', {'form': form})

def del_from_history(request, id):
    delete_task = CompletedTask.objects.get(id = id)
    delete_task.delete()
    return HttpResponseRedirect('/history')

def restore_todo(request, id):
    restore_task = CompletedTask.objects.get(id=id)
    new_task = Task.objects.create(description = restore_task.description)
    restore_task.delete()
    return HttpResponseRedirect('/history')


def edit_in_history(request, id):
    cur_task = CompletedTask.objects.get(id = id)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=cur_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/history')
    else:
        form = EditForm(instance=cur_task)
    return render(request, 'tasks/edit_task.html', {'form': form})