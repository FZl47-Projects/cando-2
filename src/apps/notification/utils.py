from django.contrib.auth import get_user_model

from .models import NotificationUser

User = get_user_model()


def create_notify_admins(type, title, kwargs):
    admins = User.super_user_objects.all()
    for admin in admins:
        n = NotificationUser.objects.create(
            type=type,
            title=title,
            to_user=admin,
            kwargs=kwargs
        )
