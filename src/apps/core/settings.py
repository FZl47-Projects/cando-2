from django.conf import settings
from django.utils.translation import gettext_lazy as _

OBJECTS = {
    'CATEGORY': {
        'default_name': _('without category')
    }
}

IMAGE = {
    'DEFAULT_IMAGE_PATH': settings.BASE_DIR / 'static/images/product-default-img.png'
}
