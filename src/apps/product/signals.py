from django.db.models.signals import post_save
from django.db import IntegrityError
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


@receiver(post_save, sender=models.BasicProduct)
def create_comment_notify_status(sender, instance, created, **kwargs):
    if created:
        # TODO: create notify when comment submited
        pass
    else:
        if instance.status == 'accepted':
            # TODO :create notify when status changed to accepted
            pass


@receiver(post_save, sender=models.CustomProduct)
def create_custom_product_status(sender, instance, created, **kwargs):
    if created:
        # create custom product status
        models.CustomProductStatus.objects.create(
            custom_product=instance,
        )


@receiver(post_save, sender=models.CustomProductStatus)
def create_custom_product_cart_item(sender, instance, created, **kwargs):
    # create custom product cart item
    if instance.status == 'accepted':
        cart_item = getattr(instance.custom_product, 'cart_item', None)
        if not cart_item:
            # create cart item
            custom_product = instance.custom_product
            models.CustomProductCart.objects.create(
                cart=custom_product.user.get_current_cart_or_create(),
                custom_product=custom_product
            )
            # TODO: should send notify for user


@receiver(post_save, sender=models.Cart)
def create_cart_status(sender, instance, created, **kwargs):
    # create cart status after payment
    if instance.get_invoice_purchase():
        # create cart status(order)
        try:
            models.CartStatus.objects.create(
                cart=instance
            )
        except (IntegrityError,):
            pass


@receiver(post_save, sender=models.CartStatus)
def create_notification_change_cart_status(sender, instance, created, **kwargs):
    # create notification after change order start(cart status)
    # TODO: should send notify for user
    pass