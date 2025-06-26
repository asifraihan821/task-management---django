from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

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
    tasks = Task.objects.all()

    #specific task
    task_3 = Task.objects.get(id=1)
    return render(request, "show_task.html", {'tasks':tasks, 'task3':task_3})