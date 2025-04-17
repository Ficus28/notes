from django import forms
from .models import Note
from django_ckeditor_5.widgets import CKEditor5Widget  # 🔥

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditor5Widget(config_name='default'),  # ✅ CKEditor5 виджет
        }