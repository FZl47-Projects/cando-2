from django.contrib import admin

from . import models

admin.site.register(models.DefaultStoreAddress)
admin.site.register(models.Address)
