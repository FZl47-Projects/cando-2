from django.db import models
from django.urls import reverse

from apps.core.models import BaseModel


class DefaultStoreAddress(BaseModel):
    """
            Singleton
            TODO: should use SingletonModel
    """
    address = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return f'default store address setting'


class Address(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.TextField()
    plate = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.user}'

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:address__detail', args=(self.id,))
