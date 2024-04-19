from django.db import models

from apps.core.mixins.models import RemovePastFileMixin
from apps.core.models import BaseModel
from apps.core.utils import get_time, random_str


def upload_file_src(instance, path):
    # TODO: add validator format
    frmt = str(path).split('.')[-1]
    tm = get_time('%Y-%m-%d')
    return f'files/{tm}/{random_str()}.{frmt}'


def upload_image_src(instance, path):
    # TODO: add validator format
    frmt = str(path).split('.')[-1]
    tm = get_time('%Y-%m-%d')
    return f'images/{tm}/{random_str()}.{frmt}'


class FileAbstract(RemovePastFileMixin, BaseModel):
    # TODO: add hashing and prevent duplicate file | feature
    FIELDS_REMOVE_FILES = ('file',)
    file = models.FileField(upload_to=upload_file_src, max_length=400)

    class Meta:
        abstract = True
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} File'


class Image(RemovePastFileMixin, BaseModel):
    # TODO: add hashing and prevent duplicate image | feature
    FIELDS_REMOVE_FILES = ('image',)
    image = models.ImageField(upload_to=upload_image_src, max_length=400, null=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} Image'

    def get_image_url(self):
        try:
            return self.image.url
        except AttributeError:
            pass
