from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
    else:
        # Заглушка для гостей
        notes = [
            {"title": "Добро пожаловать!", "content": "Создавайте заметки после регистрации"},
            {"title": "Заметка №1", "content": "Эта заметка демонстрационная и не сохраняется"},
        ]
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

@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            return redirect('home')
        else:
            return render(request, 'add_note.html', {'error': 'Все поля должны быть заполнены'})
    return render(request, 'add_note.html')


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        if title and content:
            note.title = title
            note.content = content
            note.save()
            return redirect('home')
        else:
            return render(request, 'edit_note.html', {'note': note, 'error': 'Все поля должны быть заполнены'})
    return render(request, 'edit_note.html', {'note': note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'delete_confirm.html', {'note': note})

