from django.db import models
from apps.core.utils import  get_timesince_persian


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


