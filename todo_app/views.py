from django.shortcuts import render, redirect, get_object_or_404
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

def edit_task(request, id):
    task = Task.objects.get(id = id)  # safely fetch the task
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)  # bind form to existing task
        if form.is_valid():
            form.save()
            save_tasks_to_file()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)  # pre-fill with existing data
    return render(request, 'todo_app/edit_task.html', {'form': form})

from django.db import connection

def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    save_tasks_to_file()

    # If no tasks remain, reset auto-increment counter
    if not Task.objects.exists():
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='todo_app_task';")

    return redirect('task_list')
