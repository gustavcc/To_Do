from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

def taskList(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/list.html', {'tasks':tasks})

def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})

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