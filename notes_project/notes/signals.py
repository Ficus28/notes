from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import UserSessionLog
from django.utils.timezone import now


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserSessionLog.objects.create(user=user, login_time=now())

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    last_log = UserSessionLog.objects.filter(user=user).order_by('-login_time').first()
    if last_log and not last_log.logout_time:
        last_log.logout_time = now()
        last_log.save()