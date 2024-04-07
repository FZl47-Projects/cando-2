from django.db import models
from apps.core.utils import get_time, get_timesince_persian, random_str
from apps.core.mixins.models import RemovePastFileMixin


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


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_at_timepast(self):
        return get_timesince_persian(self.created_at)

    def get_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at_timepast(self):
        return get_timesince_persian(self.updated_at)


class FileAbstract(RemovePastFileMixin, models.Model):
    # TODO: add hashing and prevent duplicate file | feature
    FIELDS_REMOVE_FILES = ('file',)
    file = models.FileField(upload_to=upload_file_src, max_length=400)

    class Meta:
        abstract = True
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} File'


class Image(RemovePastFileMixin, models.Model):
    # TODO: add hashing and prevent duplicate image | feature
    FIELDS_REMOVE_FILES = ('image',)
    image = models.ImageField(upload_to=upload_image_src, max_length=400, null=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} Image'
