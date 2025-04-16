from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    COLOR_CHOICES = [
        ('light', 'Светлый'),
        ('primary', 'Синий'),
        ('success', 'Зелёный'),
        ('warning', 'Жёлтый'),
        ('danger', 'Красный'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='light')
    image = models.ImageField(upload_to='notes_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_registration = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username