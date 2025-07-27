from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm,CreateProjectForm
from tasks.models import Task, Project, TaskDetail
from datetime import date
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from users.views import is_admin
from django.views import View
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView
from django.views.generic import CreateView


class Greetings(View):
    greetings = 'hi everyone'

    def get(self,request):
        return HttpResponse(self.greetings)
    
class Nothing(Greetings):
    greetings = 'I am asif'
    
class JustDoIt(Nothing):
    greetings = 'hi my friend'

# Create your views here.
def is_manager(user):
    return user.is_authenticated and user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='User').exists()


@user_passes_test(is_manager, login_url='no-permission')
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

@user_passes_test(is_employee,login_url='no-permission')
def employee_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')


'''CRUD Operations
    C = Create
    R = Read
    U = Update
    D = Delete
'''

"""
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
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


create_decorators = [login_required, permission_required('tasks.add_task', login_url='no-permission')]

"""
class CreateProject(CreateView):
    model = Project
    form_class = CreateProjectForm
    context_object_name = 'form'
    template_name = 'admin/create_project.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Project created Successfully.')
        return redirect( 'admin-dashboard')
    


class CreateTask(ContextMixin, LoginRequiredMixin,PermissionRequiredMixin,  View):
    """creating task..."""
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'get_post.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'get_post.html',context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():

            '''for Model Form Data'''
            task = task_form.save()
            task_detail: TaskDetail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, 'Task Created Successfully')
            context = self.get_context_data(task_form = task_form, task_detail_form = task_detail_form)
            return render(request, self.template_name, context)



"""
@login_required
@permission_required('tasks.change_task', login_url='no-permission')
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
            h
    context = {'task_form' : task_form, 'task_detail_form': task_detail_form}
    return render(request, 'get_post.html',context)


change_decorators = [permission_required('tasks.change_task', login_url='no-permission')]

"""
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'get_post.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance = self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance = self.object)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance = getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            '''for Model Form Data'''
            task = task_form.save()
            task_detail: TaskDetail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, 'Task updated Successfully')

            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)




@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    if request.method =="POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task deleted Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,'something Went Wrong')
        return redirect('manager-dashboard')


"""

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_task(request):
    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request, "show_task.html", 
    {'projects' : projects})

"""

view_project_decorators = [permission_required('projects.view_project', login_url='no-permission')]
@method_decorator(view_project_decorators, name = 'dispatch')
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html' 

    def get_queryset(self):
        queryset = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
        return queryset


@login_required
@permission_required('tasks.view_task')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method  =='POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect ('task-details', task.id)

    return render(request, 'task_details.html', {'task': task, 'status_choices':status_choices})


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_details.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context 
    
    def post(self,request,*args,**kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect ('task-details', task.id)
     


@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    
    
    return redirect('no-permission')



