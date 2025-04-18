from django import forms
from .models import Note
from django_ckeditor_5.widgets import CKEditor5Widget

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditor5Widget(config_name='default'),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Заголовок не может быть пустым.")
        if len(title.strip()) < 3:
            raise forms.ValidationError("Заголовок должен содержать минимум 3 символа.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("Содержимое не может быть пустым.")
        return content
