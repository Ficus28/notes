from django.shortcuts import render, redirect
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth import login

def home(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/home.html', {'notes': notes})

def add_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content)
        return redirect('home')
    return render(request, 'notes/add_note.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'notes/register.html')

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'notes/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'notes/login.html')
