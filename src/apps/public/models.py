from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.core.utils import random_str, get_time


def get_upload_slider_src(instance, path):
    frmt = str(path).split('.')[-1]
    tm = get_time('%Y-%m-%d')
    if not frmt in settings.PICTURE_FORMATS:
        raise ValidationError(_('Picture Format Must Be One Of %s') %
                              ', '.join(settings.PICTURE_FORMATS))
    return f'images/sliders/{tm}/{random_str()}.{frmt}'


class Slider(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_upload_slider_src)

    def __str__(self):
        return f'slider - {self.id}'

    def get_picture_url(self):
        try:
            return self.picture.url
        except (AttributeError, ValueError):
            pass
