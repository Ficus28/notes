from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse, HttpResponseForbidden
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


def home(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'home.html', {'notes': notes})
    else:
        # Гостевые (демо) заметки
        guest_notes = [
            {"title": "Добро пожаловать!", "content": "Зарегистрируйтесь, чтобы сохранять свои заметки."},
            {"title": "Пример заметки", "content": "Это демо-заметка. Зарегистрируйтесь, чтобы создать свою!"},
        ]
        return render(request, 'home.html', {'notes': guest_notes, 'guest_mode': True})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        email = request.POST.get('email').strip()

        if not username or not password or not email:
            return render(request, 'register.html', {'error': 'Заполните все поля'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Пользователь с таким именем уже существует'})

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate(request, username=username, password=password)
        if user:
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
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})
    

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm(instance=note)
    return render(request, 'edit_note.html', {'form': form, 'note': note})



@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Заметка удалена.')
        return redirect('home')
    return render(request, 'delete_confirm.html', {'note': note})

@csrf_exempt
@login_required
def custom_ckeditor_upload_view(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_path = os.path.join('uploads', upload.name)
        saved_path = default_storage.save(file_path, ContentFile(upload.read()))

        return JsonResponse({
            "url": default_storage.url(saved_path)
        })

    return HttpResponseForbidden("Не удалось загрузить изображение.")

@login_required
def profile_view(request):
    user = request.user
    password_form = PasswordChangeForm(user)
    
    if request.method == 'POST':
        if 'change_email' in request.POST:
            new_email = request.POST.get('email')
            if new_email and new_email != user.email:
                user.email = new_email
                user.save()
                messages.success(request, 'Email обновлён.')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменён.')

    return render(request, 'profile.html', {
        'user': user,
        'password_form': password_form,
    })
