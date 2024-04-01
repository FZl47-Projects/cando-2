from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.db import models

from apps.core.mixins.models import RemovePastFileMixin
from apps.core.models import BaseModel
from apps.core.utils import now_shamsi_date, convert_str_to_shamsi_date
from . import utils


class ProductManager(models.Manager):

    def get_best_sellers(self):
        # TODO: must be completed
        return self.get_queryset()

    def get_news(self):
        # TODO: must be completed
        return self.get_queryset()

    def get_suggested(self):
        # TODO: must be completed
        return self.get_queryset()

    def get_list(self):
        return self.get_queryset().filter(status='active')

    def get_inactive_list(self):
        return self.get_queryset().filter(status='inactive')

    def get_archived_list(self):
        return self.get_queryset().filter(status='archived')


class BaseProduct(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class BasicProduct(BaseProduct):
    STATUS_OPTIONS = (
        ('active', _('active')),
        ('inactive', _('inactive')),
        ('archived', _('archived')),
    )
    TYPE_OPTIONS = (
        ('simple', _('simple')),
        ('showcase', _('showcase')),
    )
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image_cover = models.ForeignKey('core.Image', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='product_cover')
    images = models.ManyToManyField('core.Image', blank=True)
    attr_category = models.ForeignKey('ProductAttrCategory', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='active')
    type = models.CharField(max_length=12, choices=TYPE_OPTIONS)

    objects = ProductManager()

    class Meta:
        ordering = ('-id',)

    def has_in_stock(self):
        return True if self.get_quantity() > 0 else False

    def get_absolute_url(self):
        return reverse('product:basic_product__detail', args=(self.id,))

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:basic_product__detail', args=(self.id,))

    def get_similar_products(self):
        return BasicProduct.objects.filter(categories__in=self.get_categories()).all()

    def get_comments(self):
        return self.comment_set.filter(status='accepted')

    def get_all_comments(self):
        return self.comment_set.all()

    def get_rate(self):
        avg = self.get_comments().aggregate(rate_avg=models.Avg('rate'))['rate_avg'] or 0
        avg = round(avg, 1)
        return avg

    def get_price(self):
        return self.productinventory.price

    def get_quantity(self):
        return self.productinventory.quantity

    def get_total_sales_count(self):
        pass

    def get_categories(self):
        return self.categories.all()

    def get_tags(self):
        return self.tags.all()

    def get_image_cover(self):
        try:
            return self.image_cover.image.url
        except Exception as e:
            # TODO: must be completed
            return '/static/images/logo.png'

    def get_images(self):
        return self.images.all()

    def get_attr_groups(self):
        if self.attr_category:
            return self.attr_category.get_groups()
        return []


class ProductInventory(BaseModel):
    product = models.OneToOneField('BasicProduct', on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f'{self.product} - {self.quantity}:{self.price}'


class ProductAttrCategory(BaseModel):
    """
        Product Attribute Category
    """
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField('ProductAttrGroup', blank=True)

    def __str__(self):
        return self.name

    def get_groups(self):
        return self.groups.all()


class ProductAttrGroup(BaseModel):
    """
        Product Attribute Group
        Examples: color, size,...
    """
    name = models.CharField(max_length=100)
    fields = models.ManyToManyField('SimpleProductAttr')

    def __str__(self):
        return self.name

    def get_fields(self):
        return self.fields.all()


class BaseProductAttr(BaseModel):
    """
        Product Attribute Field
        Examples: size(sm, md, ..) | color(black, white, ..)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class SimpleProductAttr(RemovePastFileMixin, BaseProductAttr):
    FIELDS_REMOVE_FILES = ('picture',)
    additional_price = models.PositiveBigIntegerField(default=0)
    picture = models.ImageField(upload_to=utils.get_upload_src_product_attr_pic, null=True, blank=True)

    def get_picture_url(self):

        try:
            return self.picture.url
        except ValueError:
            pass


class ProductView(BaseProduct):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('BasicProduct', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.product}'


class Category(BaseModel):
    """
        field 'default': If the default value is True, then it will be set automatically for products that do not have a category
    """

    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    class Meta:
        ordering = ('-default', '-id')

    def __str__(self):
        return self.name

    def get_products(self):
        return self.basicproduct_set.all()


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_products(self):
        return self.basicproduct_set.all()


class DiscountCoupon(BaseModel):
    code = models.CharField(max_length=30, unique=True)
    price = models.PositiveBigIntegerField()
    expire_at = models.DateField()
    count = models.PositiveBigIntegerField(default=1)
    cart_price_more = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.code

    def get_expire_at(self):
        return str(self.expire_at)

    def get_expire_at_date(self):
        return convert_str_to_shamsi_date(str(self.expire_at))

    def check_expire(self):
        if self.get_expire_at_date() > now_shamsi_date():
            return True
        return False


class ProductFavoriteList(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('BasicProduct')

    def __str__(self):
        return f'favorite list - {self.user}'


class Comment(BaseModel):
    RATE_OPTIONS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    STATUS_OPTIONS = (
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
        ('pending', _('pending')),
    )

    product = models.ForeignKey('BasicProduct', on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.SmallIntegerField(choices=RATE_OPTIONS)
    status = models.CharField(max_length=15, choices=STATUS_OPTIONS, default='pending')

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'{self.text[:20]} - {self.product}'


class FactorCakeImage(BaseModel):
    STATUS_OPTIONS = (
        ('seen', _('Seen')),
        ('unseen', _('Unseen')),
    )
    user_name = models.CharField(max_length=200)
    factor_code = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default='unseen')
    images = models.ManyToManyField('core.Image', blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.user_name

    def get_images(self):
        return self.images.all()


class Cart(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)  # user or session cart
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user


class ProductCart(BaseProduct):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('BasicProduct', on_delete=models.SET_NULL, null=True)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.cart} - {self.product}'


class ProductAttrCart(BaseProduct):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    group = models.ForeignKey('ProductAttrGroup', on_delete=models.SET_NULL, null=True)
    attr = models.ForeignKey('SimpleProductAttr', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.cart} - {self.group}|{self.attr}'


class WishList(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, null=True)  # user or session wishlist
    products = models.ManyToManyField('BasicProduct')

    def __str__(self):
        return f'{self.user} - wishlist'

