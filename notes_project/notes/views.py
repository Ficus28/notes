from django.shortcuts import render, redirect
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'notes': notes})

def add_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content)
        return redirect('home')
    return render(request, 'add_note.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Логин уже занят'})

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
