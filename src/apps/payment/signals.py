from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import NotificationUser
from apps.notification.utils import create_notify_admins
from . import models


@receiver(post_save, sender=models.PurchaseInvoice)
def create_notify_payment(sender, instance, created, **kwargs):
    if created:
        # create notify for user
        NotificationUser.objects.create(
            type='PAYMENT_SUCCESSFULLY_USER',
            to_user=instance.user,
            title=_('Payment Was Successful'),
            kwargs={
                'link': instance.get_absolute_url()
            }
        )
        # create notify for admin's
        create_notify_admins(
            type='NEW_PAYMENT_ADMIN',
            title=_('A New Payment Has Been Made'),
            kwargs={
                'link': instance.get_dashboard_absolute_url()
            }
        )
