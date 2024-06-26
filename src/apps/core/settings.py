from django.conf import settings
from django.utils.translation import gettext_lazy as _

OBJECTS = {
    'CATEGORY': {
        'default_name': _('without category')
    },
}

IMAGE = {
    'DEFAULT_IMAGE_PATH': settings.BASE_DIR / 'static/images/product-default-img.png'
}


def get_default_address():
    from apps.navigation.models import Address

    return Address.objects.filter(defaultstoreaddress__isnull=False)


def get_default_inventory():
    from apps.product.models import ProductInventoryDefault

    return ProductInventoryDefault.objects.first()
