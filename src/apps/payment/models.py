import abc
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.shortcuts import reverse

from apps.core.models import BaseModel
from apps.navigation.enums import DeliveryTime


class InvoiceBase(BaseModel):
    purchase = models.OneToOneField('PurchaseInvoice', on_delete=models.SET_NULL, null=True, blank=True)
    discount_selected = models.ForeignKey('product.DiscountCouponSelected', on_delete=models.SET_NULL, null=True,
                                          blank=True)

    @abc.abstractmethod
    def get_total_price(self):
        pass

    def get_discount_price(self):
        if self.discount_selected:
            return self.discount_selected.discount.price
        return 0

    class Meta:
        abstract = True


class ManualInvoice(InvoiceBase):
    cart = models.ForeignKey('product.Cart', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveBigIntegerField()

    def get_total_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('public:cart')


class Invoice(InvoiceBase):
    cart = models.OneToOneField('product.Cart', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey('navigation.Address', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_time = models.CharField(max_length=20, choices=DeliveryTime.choices)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def get_total_price(self):
        if self.cart:
            self.cart.delivery_time = self.delivery_time
            return self.cart.get_total_price()
        return _('Unspecified Price')

    def get_absolute_url(self):
        return reverse('public:cart')

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:invoice__detail', args=(self.id,))

    def get_purchase_url(self):
        return reverse('payment:invoice__purchase', args=(self.id,))


class PurchaseInvoice(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)
    tracking_code = models.CharField(max_length=40)
    bank_name = models.CharField(max_length=20)
    price_paid = models.PositiveBigIntegerField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.tracking_code

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:purchase_invoice__detail', args=(self.id,))

    def get_absolute_url(self):
        return self.get_dashboard_absolute_url()
