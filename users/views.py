from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,CustomRegistrationForm
from django.contrib import messages
from users.forms import LoginForm


# Create your views here.
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


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')