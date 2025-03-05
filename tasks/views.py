from django.shortcuts import render
from .models import Task
from .forms import TodoForm
from django.http import HttpResponseRedirect
# Create your views here.

def get_page(request):
    tasks = Task.objects.all()
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            new_tasks = Task.objects.create(description = form.cleaned_data['add'])
            return HttpResponseRedirect('/')
    return render(request, 'tasks/cur_tasks.html', context = {'tasks': tasks, 'form': form})


