from django.contrib.auth import get_user_model

from .models import NotificationUser

user = get_user_model()


def create_notify_admins(type, title, kwargs):
    admins = user.objects.filter(role__in=['super_user'])
    notifications = []
    for admin in admins:
        n = NotificationUser(
            type=type,
            title=title,
            to_user=admin,
            kwargs=kwargs
        )
        notifications.append(n)
    NotificationUser.objects.bulk_create(notifications)
