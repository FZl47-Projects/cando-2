from django.contrib import admin
from . import models


admin.site.register(models.BasicProduct)
admin.site.register(models.ProductInventory)
admin.site.register(models.ProductInventoryDefault)
admin.site.register(models.ProductAttrGroup)
admin.site.register(models.ProductAttrCategory)
admin.site.register(models.SimpleProductAttr)
admin.site.register(models.ProductAttrSelected)
admin.site.register(models.CustomProduct)
admin.site.register(models.CustomProductStatus)
admin.site.register(models.CustomProductCakeAttrCategory)
admin.site.register(models.CustomProductSweetsAttrCategory)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.DiscountCoupon)
admin.site.register(models.FactorCakeImage)
admin.site.register(models.WishList)
admin.site.register(models.Cart)
admin.site.register(models.CartStatus)
admin.site.register(models.ProductCart)
