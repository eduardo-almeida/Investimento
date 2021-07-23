from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .forms import TaskForm
from coins.forms import CoinForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
import datetime

from .models import Task


@login_required
def taskList(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')

    if search:
        tasks = Task.objects.filter(coin__nome__icontains=search)
    elif filter:
        tasks = Task.objects.filter(coin__modalidade=filter)
    else:
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(tasks_list, 3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def taskList2(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')
    
    fixa = Task.objects.filter(modalidade='renda fixa', user=request.user).count()
    variavel = Task.objects.filter(modalidade='renda variável', user=request.user).count()
    cripto = Task.objects.filter(modalidade='cripto', user=request.user).count()

    if search:
        tasks = Task.objects.filter(nome__icontains=search, user=request.user)
    elif filter:
        tasks = Task.objects.filter(modalidade=filter, user=request.user)
    else:
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(tasks_list, 3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request, 'tasks/list.html', {'tasks': tasks, 'fixa': fixa, 'variavel': variavel, 'cripto': cripto})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})    

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if (form.is_valid()):
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    if (request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if (form.is_valid()):
            task = form.save(commit=False)

            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, "Moeda deletada com sucesso!")
    return redirect('/')
