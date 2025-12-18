from django.shortcuts import render, redirect
from django.utils import timezone
from .models import StudentGeneralTask, Task
from users.models import User
from django.contrib import messages
from django.db import IntegrityError

def tasklist_page(request):
    today = timezone.localdate()

    student_tasks = (
        StudentGeneralTask.objects
        .select_related("id_gen_task")
        .filter(id_user=request.user)
    )

    # Compute days remaining until deadline for each student task.
    # Treat overdue tasks (negative days) as urgent as well.
    def days_until(st):
        # Prefer per-student deadline if present, otherwise fall back to the generic task deadline
        try:
            deadline = None
            if getattr(st, 'deadline', None):
                deadline = st.deadline
            elif getattr(st, 'id_gen_task', None) and getattr(st.id_gen_task, 'deadline', None):
                deadline = st.id_gen_task.deadline

            if not deadline:
                return 99999

            return (deadline - today).days
        except Exception:
            return 99999

    tasks_sorted = sorted(student_tasks, key=days_until)

    # Define urgent as tasks overdue or within the next 2 days.
    urgent_tasks = [st for st in tasks_sorted if days_until(st) <= 2]
    # Keep only first two urgent tasks for the compact urgent area
    urgent_tasks = urgent_tasks[:2]
    # Keep only unique entries and keep ordering; remaining tasks are "other"
    other_tasks = [st for st in tasks_sorted if st not in urgent_tasks]

    return render(
        request,
        "tasks/tasklist.html",
        {
            "urgent_tasks": urgent_tasks,
            "other_tasks": other_tasks,
            "student": request.user,
        }
    )


def all_tasks_admin(request):
    # Only admins should access this view
    if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
        return redirect('login')
    
    tasks = Task.objects.all().order_by('title')
    
    return render(request, 'tasks/all_tasks.html', {
        'tasks': tasks,
    })


def assign_task(request):
    # only admins
    if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
        return redirect('login')

    if request.method == 'GET':
        # Show available tasks and student filters
        tasks_qs = Task.objects.all().order_by('title')
        # distinct groups and countries from users
        groups = User.objects.values_list('group', flat=True).distinct()
        countries = User.objects.values_list('citizenship', flat=True).distinct()
        students = User.objects.filter(role='student').order_by('surname', 'first_name')
        selected_task = request.GET.get('task_id')
        return render(request, 'tasks/assign_task_modal.html', {
            'tasks': tasks_qs,
            'groups': [g for g in groups if g],
            'countries': [c for c in countries if c],
            'students': students,
            'selected_task_id': int(selected_task) if selected_task else None,
        })

    # POST - perform assignment
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        assign_type = request.POST.get('assign_type')  # 'group' | 'country' | 'student' | 'all'
        value = request.POST.get('value')  # group name or country or student id

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            messages.error(request, 'Задача не найдена')
            return redirect('all_tasks')

        created = 0
        errors = 0

        if assign_type == 'group' and value:
            targets = User.objects.filter(role='student', group=value)
        elif assign_type == 'country' and value:
            targets = User.objects.filter(role='student', citizenship=value)
        elif assign_type == 'student' and value:
            targets = User.objects.filter(role='student', id_user=value)
        elif assign_type == 'all':
            targets = User.objects.filter(role='student')
        else:
            targets = User.objects.none()

        for u in targets:
            try:
                sgt = StudentGeneralTask.objects.create(
                    id_user=u,
                    id_gen_task=task,
                    status='not_done',
                )
                created += 1
            except IntegrityError:
                # skip duplicates
                errors += 1
            except Exception:
                errors += 1

        messages.success(request, f'Назначено: {created} задач(и). Пропущено: {errors}.')
        return redirect('all_tasks')