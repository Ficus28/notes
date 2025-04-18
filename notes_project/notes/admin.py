from django.contrib import admin
from .models import Note
from .models import UserSessionLog

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at') 
    list_filter = ('user',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Note, NoteAdmin)

@admin.register(UserSessionLog)
class UserSessionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time')
    list_filter = ('user',)
    ordering = ('-login_time',)
