from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Min,Max,Avg

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

def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()

    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():

            '''for Model Form Data'''
            form.save()

            return render(request, 'get_post.html', {'form':form, 'massage': 'Task Added Successfully'})



            ''' for Django form Data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(title=title, description=description, due_date= due_date)
            
            # #assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)  

            # return HttpResponse("task added successfully")
            
    context = {'form' : form}
    return render(request, 'get_post.html',context)

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