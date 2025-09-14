from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

# Save tasks to a text file
def save_tasks_to_file():
    tasks = Task.objects.all()
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task.title + "\n")

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            save_tasks_to_file()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/add_task.html', {'form': form})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    save_tasks_to_file()
    return redirect('task_list')
