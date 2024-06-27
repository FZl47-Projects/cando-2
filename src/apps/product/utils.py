from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.core.utils import random_str, get_time


def get_upload_src_product_attr_pic(instance, path):
    frmt = str(path).split('.')[-1]
    tm = get_time('%Y-%m-%d')
    if not frmt in settings.PICTURE_FORMATS:
        raise ValidationError(_('Picture Format Must Be One Of %s') %
                              ', '.join(settings.PICTURE_FORMATS))
    return f'images/product-attr/{tm}/{random_str()}.{frmt}'
