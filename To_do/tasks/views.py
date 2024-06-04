from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def taskList(request):
    
    # search system
    search = request.GET.get('search')
    
    if search:
        
        tasks = Task.objects.filter(title__icontains=search,description__icontains=search)
    else:

        # definir variavel com todos os objetos
        tasks_list = Task.objects.all().order_by('-created_at')
        # definir quabtos registros por pagina
        paginator = Paginator(tasks_list, 5)
        # numero da pagina ira vir atraves da url
        page = request.GET.get('page')
        # definir variavel final
        tasks = paginator.get_page(page)
        
    return render(request, 'tasks/list.html', {'tasks':tasks})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.save()
            return redirect('/')
        else:
            form = TaskForm()
            return render(request, 'tasks/newtask.html', {'form': form})
    else:
        form = TaskForm()
        return render(request, 'tasks/newtask.html', {'form': form})

@login_required
def taskEdit(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)
    # pega o objeto de acordo com o id e mostra para o usuário poder editá-lo
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/taskedit.html', {'form': form, 'task': task})
    else:
        return render(request, 'tasks/taskedit.html', {'form': form, 'task': task})

@login_required
def taskDelete(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    
    messages.info(request, 'Tarefa deletado com sucesso!')
    
    return redirect('/')