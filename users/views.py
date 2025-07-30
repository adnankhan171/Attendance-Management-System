from django.shortcuts import render, redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('home')  # Redirect to the home page or another page
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:home')  # Redirect to the home page after successful login
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# @never_cache
@login_required
def home(request):
    return render(request, 'users/home.html')

def landing_page(request):
    return render(request, 'users/landing_page.html')



def logout_view(request):
    logout(request)
    return redirect('landing_page')  # Redirect to your login page or home page


