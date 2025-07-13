from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task, Project, TaskDetail
from datetime import date
from django.db.models import Q,Count
from django.contrib import messages

# Create your views here.

def manager_dashboard(request):

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status = 'COMPLETED').count()
    # in_progress_task = Task.objects.filter(status = 'IN_PROGRESS').count()
    # pending_task = Task.objects.filter(status = 'PENDING').count()

    type = request.GET.get('type','all')

    #retreiving task data
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type =='in_progress':
        tasks = base_query.filter(status = 'IN_PROGRESS')
    elif type =='pending':
        tasks = base_query.filter(status = 'PENDING')
    elif type =='all':
        tasks = base_query.all()
    
    

    counts = Task.objects.aggregate(
        total = Count('id'),
        completed = Count('id',filter = Q(status = 'COMPLETED')),
        in_progress = Count('id',filter = Q(status = 'IN_PROGRESS')),
        pending = Count('id',filter = Q(status = 'PENDING'))
    )

    context = {
        'tasks':tasks,
        'counts':counts
    }
    return render(request, "dashboard/manager-dashboard.html", context)

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')

def test(request):
    names =  ["asif", "rahman", "john","mr.x"]
    count=0
    for name in names:
        count +=1
    context = {
        "names" :names,
        "age" : 23,
        "count" : count
    }
    return render(request, 'test.html' , context)


'''CRUD Operations
    C = Create
    R = Read
    U = Update
    D = Delete
'''


def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():

            '''for Model Form Data'''
            task = task_form.save()
            task_detail: TaskDetail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, 'Task Created Successfully')

            return redirect('create-task')
            
    context = {'task_form' : task_form, 'task_detail_form': task_detail_form}
    return render(request, 'get_post.html',context)

def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance = task)

    if task.details:
        task_detail_form = TaskDetailModelForm(instance = task.details)

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance = task)
        task_detail_form = TaskDetailModelForm(request.POST, instance = task.details)
        if task_form.is_valid() and task_detail_form.is_valid():

            '''for Model Form Data'''
            task = task_form.save()
            task_detail: TaskDetail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, 'Task updated Successfully')

            return redirect('update-task', id)
            
    context = {'task_form' : task_form, 'task_detail_form': task_detail_form}
    return render(request, 'get_post.html',context)


def delete_task(request, id):
    if request.method =="POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task deleted Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,'something Went Wrong')
        return redirect('manager-dashboard')


def view_task(request):
    #for retrieving all data
    # tasks = Task.objects.all()

    # #specific task 
    # task_3 = Task.objects.get(id=1)

    # tasks = Task.objects.filter(status="COMPLETED")

    # tasks = Task.objects.filter(due_date = date.today())

    # tasks = Task.objects.filter(title__icontains='c', status='PENDING')
    # tasks = Task.objects.filter(Q(status = 'PENDING')| Q(status='IN_PROGRESS'))

    # tasks = Task.objects.filter(status='PENDING').exists()

    """"SELECT_RELATED QUERY"""

    # tasks = TaskDetail.objects.select_related('task').all()

    # tasks = Task.objects.select_related('p roject').all()
    
    """prefetch_related"""
    # tasks = Project.objects.prefetch_related('task_set').all()
    
    # tasks = Task.objects.prefetch_related('assigned_to').all()

    """aggragate functions"""

    # task_count = Task.objects.aggregate(num_task = Count('id'))

    """annotate functiion"""

    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')

    return render(request, "show_task.html", 
    {'projects' : projects})