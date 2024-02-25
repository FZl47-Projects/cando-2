from django.contrib import admin
from . import models


@admin.register(models.CakeProduct)
class CakeProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'selling_price', 'on_display')
