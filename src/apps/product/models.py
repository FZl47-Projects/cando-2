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
        return self.get_queryset().all()

    def get_active_list(self):
        return self.get_queryset().filter(status='active')

    def get_inactive_list(self):
        return self.get_queryset().filter(status='inactive')

    def get_archived_list(self):
        return self.get_queryset().filter(status='archived')


class BaseProduct(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

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
        if self.get_quantity() > 0 and self.get_price() > 0:
            return True
        return False

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


class ProductAttrSelected(BaseModel):
    group = models.ForeignKey('ProductAttrGroup', on_delete=models.CASCADE)
    attr = models.ForeignKey('SimpleProductAttr', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group} - {self.attr}'


class CustomProduct(BaseModel):
    TYPE_OPTIONS = (
        ('picture_on', _('Picture On')),
        ('model_on', _('Model On')),
    )
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=12, choices=TYPE_OPTIONS)
    receipt_date = models.DateTimeField()
    images = models.ManyToManyField('core.Image')
    writing_on = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    attrs_selected = models.ManyToManyField('ProductAttrSelected')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"#{self.id} custom product | {self.user or '-'}"

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:custom_product__detail', args=(self.id,))

    def get_attributes(self):
        return self.attrs_selected.all()

    def get_attributes_price(self):
        attributes = self.get_attributes()
        price = attributes.aggregate(price_total=models.Sum('attr__additional_price'))['price_total'] or 0
        return price

    def get_images(self):
        return self.images.all()

    def get_image_cover(self):
        try:
            return self.get_images().first().image.url
        except ValueError:
            pass

    def get_price(self):
        try:
            return self.status.price
        except AttributeError:
            return None

    def get_total_price(self):
        # return self.get_price() * 1 // quantity
        return self.get_price()


class CustomProductStatus(BaseModel):
    STATUS_OPTIONS = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
    )
    status = models.CharField(max_length=12, choices=STATUS_OPTIONS, default='pending')
    custom_product = models.OneToOneField('CustomProduct', on_delete=models.CASCADE, related_name='status')
    note = models.TextField(null=True, blank=True)
    price = models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return f'{self.status} - {self.custom_product}'


class CustomProductCart(BaseModel):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    custom_product = models.OneToOneField('CustomProduct', on_delete=models.CASCADE, related_name='cart_item')

    def __str__(self):
        return f'{self.cart} - {self.custom_product}'


class CustomProductAttrCategory(BaseModel):
    """
        Singleton
        TODO: should use SingletonModel
    """
    groups = models.ManyToManyField('ProductAttrGroup', blank=True)

    def __str__(self):
        return f'custom product attr category setting'

    def get_groups(self):
        return self.groups.all()


class ProductView(BaseModel):
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


class Comment(BaseModel):
    RATE_OPTIONS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    STATUS_OPTIONS = (
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('pending', _('Pending')),
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

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:comment__detail', args=(self.id,))


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

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:factor_cake_image__detail', args=(self.id,))

    def get_images(self):
        return self.images.all()


class Cart(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)  # user or session cart
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user or 'session cart'

    def get_products(self):
        return self.productcart_set.all()

    def get_custom_products(self):
        return self.customproductcart_set.all()

    def get_all_products_count(self):
        return self.get_custom_products().count() + self.get_products().count()

    def get_price(self):
        # basic product price
        products = self.get_products()
        basic_product_price = 0
        for product in products:
            basic_product_price += product.get_total_price()
        # custom product price
        custom_products = self.get_custom_products()
        custom_product_price = 0
        for product in custom_products:
            custom_product_price += product.custom_product.get_total_price()
        return basic_product_price + custom_product_price

    def get_total_price(self):
        # TODO: count discount and ..
        return self.get_price()

    @classmethod
    def get_session_cart(cls, request):
        def create_cart(*args, **kwargs):
            return Cart.objects.create(*args, **kwargs)

        if not 'cart_id' in request.session:
            # create object cart
            cart = create_cart()
        else:
            cart_id = request.session['cart_id']
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                # invalid cart session
                cart = create_cart()

        request.session['cart_id'] = cart.id
        return cart


class ProductCart(BaseModel):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('BasicProduct', on_delete=models.SET_NULL, null=True)
    attrs_selected = models.ManyToManyField('ProductAttrSelected')
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.cart} - {self.product}'

    def get_attrs(self):
        return self.attrs_selected.all()

    def get_total_price(self):
        return self.product.get_price() * self.quantity


class WishList(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, null=True)  # user or session wishlist
    products = models.ManyToManyField('BasicProduct')

    def __str__(self):
        return f'{self.user} - wishlist'

    def get_products(self):
        return self.products.all()

    @classmethod
    def get_session_wishlist(cls, request):
        def create_wishlist(*args, **kwargs):
            return WishList.objects.create(*args, **kwargs)

        if not 'wishlist_id' in request.session:
            # create object wishlist
            wishlist = create_wishlist()
        else:
            wishlist_id = request.session['wishlist_id']
            try:
                wishlist = WishList.objects.get(id=wishlist_id)
            except WishList.DoesNotExist:
                # invalid wishlist session
                wishlist = create_wishlist()

        request.session['wishlist_id'] = wishlist.id
        return wishlist
