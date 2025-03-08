from django.shortcuts import render
from .models import Task, CompletedTask
from .forms import TodoForm
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
# Create your views here.

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
    return HttpResponseRedirect('/')


