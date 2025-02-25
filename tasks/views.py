from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, CustomUserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.db.models import Q

@login_required
def task_list(request):
    query = request.GET.get('q', '')  # Captura el texto de búsqueda
    priority_filter = request.GET.get('priority', '')  # Captura el filtro de prioridad
    status_filter = request.GET.get('status', '')  # Captura el filtro de estado

    # Filtra las tareas que pertenecen al usuario actual
    tasks = Task.objects.filter(user=request.user)

    # Si hay un término de búsqueda, filtra por título o descripción
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Filtra por prioridad si el usuario seleccionó una opción
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # Filtra por estado si el usuario seleccionó una opción
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'query': query,
        'priority_filter': priority_filter,
        'status_filter': status_filter
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            
            # Enviar correo
            send_mail(
                'Nueva Tarea Creada',
                f'Has agregado una nueva tarea: {task.title}',
                'tuemail@gmail.com',
                [request.user.email],
                fail_silently=False,
            )

            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})