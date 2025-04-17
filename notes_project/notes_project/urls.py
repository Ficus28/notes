from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_ckeditor_5.views import upload_file
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path("ckeditor5/image_upload/", login_required(upload_file), name="ckeditor5_upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
