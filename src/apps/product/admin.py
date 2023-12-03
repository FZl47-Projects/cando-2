from django.contrib import admin
from . import models

admin.site.register(models.CustomOrderProduct)
admin.site.register(models.Order)
admin.site.register(models.Category)
admin.site.register(models.Cart)
admin.site.register(models.CartStatus)
admin.site.register(models.ShowCase)
admin.site.register(models.Factor)
admin.site.register(models.FactorPayment)
admin.site.register(models.ProductFavoriteList)
