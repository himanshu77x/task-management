from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Task, Profile
from .forms import TaskForm
from django.contrib import messages

# -------------------
# Dashboard View
# -------------------
def dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})


# -------------------
# Create Task View
# -------------------
from django.contrib.auth.models import User

def create_task(request):
    employees = User.objects.all()  # abhi ke liye sabhi users dikha rahe hain
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_id = request.POST['assigned_to']
        priority = request.POST['priority']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        task_type = request.POST['task_type']

        assigned_to = User.objects.get(id=assigned_to_id)
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            start_date=start_date,
            end_date=end_date,
            task_type=task_type,
            status=status
        )
        return redirect('dashboard')

    return render(request, 'tasks/create_task.html', {'employees': employees})


# -------------------
# Edit Task View
# -------------------
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    employees = User.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task, 'employees': employees})


# -------------------
# Delete Task View
# -------------------
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('dashboard')
