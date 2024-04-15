from django.contrib import admin

from . import models

admin.site.register(models.PurchaseInvoice)
admin.site.register(models.Invoice)
admin.site.register(models.ManualInvoice)
