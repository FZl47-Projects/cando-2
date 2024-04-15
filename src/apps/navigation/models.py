from django.db import models

from apps.core.models import BaseModel


class Address(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.TextField()
    plate = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.user}'
