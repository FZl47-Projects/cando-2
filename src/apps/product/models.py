from django.utils.translation import gettext as _
from django.shortcuts import reverse
from django.db import models

from .utils import product_images_path
from apps.core.models import BaseModel


# BaseProducts model
class BaseProduct(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)

    price = models.PositiveIntegerField(_('Price'), default=0, help_text=_('Per 1Kg'))
    discount = models.PositiveSmallIntegerField(_('Discount'), default=0, help_text=_('Percentage'))
    selling_price = models.PositiveIntegerField(_('Selling price'), default=0, help_text=_('Final price to pay'))

    is_active = models.BooleanField(_('Is active'), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


# ProductCategories model
class Category(BaseModel):
    title = models.CharField(_('Category title'), max_length=128)

    class Meta:
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')

    def __str__(self):
        return self.title


# Cake's Cream model
class CakeCream(BaseModel):
    title = models.CharField(_('Title'), max_length=128)
    added_price = models.PositiveIntegerField(_('Cake added price'), default=0)

    class Meta:
        verbose_name = _('Cake cream')
        verbose_name_plural = _('Cake creams')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.title} - {self.added_price}'


# Cake's Sponges model
class CakeSponge(BaseModel):
    title = models.CharField(_('Title'), max_length=128)
    added_price = models.PositiveIntegerField(_('Cake added price'), default=0)

    class Meta:
        verbose_name = _('Cake sponge')
        verbose_name_plural = _('Cake sponges')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.title} - {self.added_price}'


# Cake's fillings model
class CakeFilling(BaseModel):
    title = models.CharField(_('Title'), max_length=128)
    added_price = models.PositiveIntegerField(_('Cake added price'), default=0)

    class Meta:
        verbose_name = _('Cake filling')
        verbose_name_plural = _('Cake fillings')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.title} - {self.added_price}'


# Tags model
class Tag(BaseModel):
    title = models.CharField(_('Tag title'), max_length=128)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title


# Weights model
class Weight(BaseModel):
    weight = models.DecimalField(_('Weight'), default=1, max_digits=4, decimal_places=1)
    description = models.CharField(_('Short description'), max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = _('Weight')
        verbose_name_plural = _('Weights')

    def __str__(self):
        return f'{self.weight} {self.get_description()}'

    def get_description(self):
        if self.description:
            return f'({self.description})'
        return ''


# CakeProducts model
class CakeProduct(BaseProduct):
    category = models.ManyToManyField(Category, related_name='cake_products', verbose_name=_('Category'))
    code = models.CharField(_('Product code'), max_length=64, null=True, blank=True)

    on_display = models.BooleanField(_('is in display'), default=False)  # Today's sell
    selling_weight = models.DecimalField(_('Selling weight'), max_digits=4, decimal_places=1, null=True, blank=True)  # Static weight by admin
    selling_stock = models.PositiveIntegerField(_('Stock'), default=0, null=True, blank=True)  # Selling stock when on display

    # Properties (customizable)
    weights = models.ManyToManyField(Weight, related_name='cake_products', verbose_name=_('Weights'))
    cream = models.ForeignKey(CakeCream, on_delete=models.SET_NULL, verbose_name=_('Cream'), null=True, blank=True)
    sponge = models.ForeignKey(CakeSponge, on_delete=models.SET_NULL, verbose_name=_('Sponge'), null=True, blank=True)
    filling = models.ForeignKey(CakeFilling, on_delete=models.SET_NULL, verbose_name=_('Filling'), null=True, blank=True)

    # Additional info
    tags = models.ManyToManyField(Tag, related_name='cake_tags', verbose_name=_('Tags'))

    class Meta:
        verbose_name = _('Cake product')
        verbose_name_plural = _('Cake products')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.code} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = 'CC' + self.id

        super().save(*args, **kwargs)

    def get_images(self):
        return self.cake_images.all()

    def get_first_image(self):
        return self.cake_images.first()


# Cake Images model
class CakeImage(BaseModel):
    product = models.ForeignKey(CakeProduct, on_delete=models.CASCADE, related_name='cake_images', verbose_name=_('Product'))
    image = models.ImageField(_('Product image'), upload_to=product_images_path)

    class Meta:
        verbose_name = _('Cake image')
        verbose_name_plural = _('Cake images')

    def __str__(self):
        return f'{self.id} - {self.product.title}'

    def get_image_url(self):
        if self.image:
            return self.image.url
