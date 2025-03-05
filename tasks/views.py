from django.shortcuts import render
from .models import Task
from .forms import TodoForm
# Create your views here.

def get_page(request):
    tasks = Task.objects.all()
    form = TodoForm()
    return render(request, 'tasks/cur_tasks.html', context = {'tasks': tasks, 'form': form})
# def show_
