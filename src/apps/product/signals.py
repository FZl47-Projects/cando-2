from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.BasicProduct)
def create_basic_product_inventory(sender, instance, created, **kwargs):
    if created:
        # create product inventory
        models.ProductInventory.objects.create(
            product=instance,
            # TODO: should be use default config (by admin)
            quantity=0,
            price=0
        )
