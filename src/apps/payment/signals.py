from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.PurchaseInvoice)
def create_notify_payment(sender, instance, created, **kwargs):
    if created:
        # TODO: send notify
        pass
