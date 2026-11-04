from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from .models import *

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        redirect('login')
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {
                'message': 'Invalid credentials.'
            })
    else:
        return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if len(password) < 8:
            return render(request, 'register.html', {
                'message': 'Password too short.'
            })
        timezone = request.POST['timezone']
        try:
            user = User.objects.create_user(username, email, password, timezone=timezone)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'register.html')