from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,EditProfileForm,CustomRegistrationForm, AssignedRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView,CreateView,ListView,FormView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()

# Create your views here.

"""

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user = self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['form'] = self.form_class(instance=self.object, userprofile=user_profile)

        return context
    
    def form_valid(self,form):
        form.save(commit=True)
        return redirect('profile')
        
        """

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def form_valid(self,form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):

    form = CustomRegistrationForm()

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, 'a confirmation mail sent to your email. please check')
            return redirect('sign-in')
        else:
            print('form invalid')
    return render(request, 'registration/register.html',{ 'form':form})


"""
def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

"""


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        # ✅ context['name'] = f'{user.first_name} {user.last_name}'
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image


        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context






class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'A Reset email sent. Please check your email .')

        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, 'Password reset successfully. ')

        return super().form_valid(form)



@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid id or token')
        
    except User.DoesNotExist:
        return HttpResponse('user not found') 

"""

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'NO group assigned'
    return render(request, 'admin/dashboard.html', {'users':users})



"""
@method_decorator(user_passes_test(is_admin,login_url='no-permission'),name='dispatch')
class AdminDashboard(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.prefetch_related(Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'NO group assigned'

        context['users'] = users
        return context


"""

@user_passes_test(is_admin, login_url='no-permission')
def assigned_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignedRoleForm()

    if request.method == 'POST':
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # removes old roels
            user.groups.add(role)
            messages.success(request, f'user {user.username} has been asigned to the {role.name} role')
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {'form': form})



"""
@method_decorator(user_passes_test(is_admin,login_url='no-permission'), name='dispatch')
class AssignRole(UpdateView):
    model = User
    form_class = AssignedRoleForm
    context_object_name = 'form'
    template_name = 'admin/assign_role.html'
    pk_url_kwarg = 'user_id'
 
    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        user = self.object
        user.groups.clear() # removes old roels
        user.groups.add(role)
        messages.success(self.request,f'user {user.username} has been asigned to the {role.name} role')
        return redirect('admin-dashboard')


@method_decorator(user_passes_test(is_admin,login_url='no-permission'), name='dispatch')
class AssignRole2(FormView):

    form_class = AssignedRoleForm
    template_name = 'admin/assign_role.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User,pk=kwargs.get('user_id'))
        return super().dispatch(request, *args, **kwargs)
 
    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        self.user.groups.clear() # removes old roels
        self.user.groups.add(role)
        messages.success(self.request,f'user {self.user.username} has been asigned to the {role.name} role')
        return redirect('admin-dashboard')
    

"""
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been added successfully')
            return redirect('create-group')
    
    return render(request, 'admin/create_group.html', {'form': form})

"""
@method_decorator(user_passes_test(is_admin,login_url='no-permission'), name='dispatch')
class CreateGroup(CreateView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'

    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been added successfully')
            return redirect('create-group')
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
        

"""

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups':groups})



"""

@method_decorator(user_passes_test(is_admin,login_url='no-permission'), name='dispatch')
class GroupList(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()