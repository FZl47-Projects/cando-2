from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.db import IntegrityError
from django.dispatch import receiver

from apps.core.utils import log_event
from apps.core.settings import get_default_inventory
from apps.notification.models import NotificationUser
from apps.notification.utils import create_notify_admins
from . import models


@receiver(post_save, sender=models.BasicProduct)
def create_basic_product_inventory(sender, instance, created, **kwargs):
    if created:
        # create product inventory
        quantity = 0
        price = 0
        default_inv = get_default_inventory()
        if default_inv:
            quantity = default_inv.quantity
            price = default_inv.price
        models.ProductInventory.objects.create(
            product=instance,
            quantity=quantity,
            price=price
        )


@receiver(post_save, sender=models.Comment)
def create_comment_notify_status(sender, instance, created, **kwargs):
    if created:
        NotificationUser.objects.create(
            type='COMMENT_SUBMITED_USER',
            title=_('Comment Has Been Submited'),
            to_user=instance.user
        )
    else:
        if instance.status == 'accepted':
            NotificationUser.objects.create(
                type='COMMENT_PRODUCT_ACCEPTED_USER',
                title=_('Comment Product Accepted'),
                to_user=instance.user,
            )
        elif instance.status == 'rejected':
            NotificationUser.objects.create(
                type='COMMENT_PRODUCT_REJECTED_USER',
                title=_('Comment Product Rejected'),
                to_user=instance.user,
            )


@receiver(post_save, sender=models.FactorCakeImage)
def create_factor_cake_image(sender, instance, created, **kwargs):
    if created:
        # create notification for admins
        create_notify_admins('FACTOR_CAKE_IMAGE_CREATED_ADMIN', _('Factor Cake Image Created'), kwargs={
            'link': instance.get_dashboard_absolute_url(),
        })


@receiver(post_save, sender=models.CustomProductCake)
def create_custom_product_cake_status(sender, instance, created, **kwargs):
    if created:
        # create custom product status
        models.CustomProductStatus.objects.create(
            custom_product=instance,
        )
        # create notification for admins
        create_notify_admins('CUSTOM_PRODUCT_CREATED', _('Custom Product Created'), kwargs={
            'custom_product_link': instance.get_dashboard_absolute_url(),
        })


@receiver(post_save, sender=models.CustomProductSweets)
def create_custom_product_sweets_status(sender, instance, created, **kwargs):
    if created:
        # create custom product status
        models.CustomProductStatus.objects.create(
            custom_product=instance,
        )
        # create notification for admins
        create_notify_admins('CUSTOM_PRODUCT_CREATED', _('Custom Product Created'), kwargs={
            'custom_product_link': instance.get_dashboard_absolute_url(),
        })


@receiver(post_save, sender=models.CustomProductStatus)
def create_custom_product_cart_item(sender, instance, created, **kwargs):
    # create custom product cart item
    cart_item = getattr(instance.custom_product, 'cart_item', None)
    if cart_item:
        return
    custom_product = instance.custom_product
    cart = custom_product.user.get_current_cart_or_create()
    if instance.status == 'accepted':
        # create cart item
        models.CustomProductCart.objects.create(
            cart=cart,
            custom_product=custom_product
        )
        if not cart.user:
            return
        NotificationUser.objects.create(
            type='CUSTOM_PRODUCT_ADDED_TO_CART',
            title=_('Custom Product Added To Cart'),
            to_user=cart.user,
            kwargs={
                'link': cart.get_absolute_url()
            }
        )
    elif instance.status == 'rejected':
        NotificationUser.objects.create(
            type='CUSTOM_PRODUCT_STATUS_REJECTED',
            title=_('Custom Product Status Rejected'),
            to_user=cart.user,
            kwargs={
                'link': cart.get_absolute_url()
            }
        )


@receiver(post_save, sender=models.Cart)
def create_cart_status(sender, instance, created, **kwargs):
    # create cart status(order) after payment
    if not instance.get_invoice_purchase():
        return
    try:
        models.CartStatus.objects.create(
            cart=instance
        )
    except (IntegrityError,):
        log_event(_('There Is Some Issue In Cart Status Creation'), 'ERROR', exc_info=True)


@receiver(post_save, sender=models.CartStatus)
def create_notification_change_cart_status(sender, instance, created, **kwargs):
    # create notification after change order status(cart status)
    user = instance.cart.user
    if not user:
        return
    NotificationUser.objects.create(
        type='CART_STATUS_UPDATED',
        title=_('Cart Status Updated'),
        to_user=user,
        kwargs={
            'link': instance.cart.get_absolute_url(),
            'status': instance.get_status_display()
        }
    )
