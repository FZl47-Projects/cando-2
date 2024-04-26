from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.db import models

from apps.core.mixins.models import RemovePastFileMixin
from apps.core.models import BaseModel
from apps.core.utils import now_shamsi_date, convert_str_to_shamsi_date
from . import utils


class ProductManager(models.Manager):

    def get_nr_user_qs(self):
        #  return querySet for (normal user)
        return self.get_queryset().filter(status='active')

    def get_best_sellers(self):
        return self.get_queryset().order_by('-productcart__productsold__count').distinct()

    def get_news(self):
        return self.get_queryset().order_by('-id')

    def get_showcases(self):
        return self.get_nr_user_qs().filter(type='showcase')

    def get_suggested(self):
        return self.get_queryset().annotate(visit=models.Count('productview')).order_by('-visit')

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
    image_cover = models.ForeignKey('storage.Image', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='product_cover')
    images = models.ManyToManyField('storage.Image', blank=True)
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
        return BasicProduct.objects.get_active_list().filter(categories__in=self.get_categories()).all()

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

    def get_sales(self):
        return ProductSold.objects.filter(product_selected__product=self)

    def get_total_sales_count(self):
        return self.get_sales().count()

    def get_total_sales_price(self):
        return self.get_sales().aggregate(total=models.Sum('price'))['total'] or 0

    def get_categories(self):
        return self.categories.all()

    def get_tags(self):
        return self.tags.all()

    def get_image_cover(self):
        try:
            return self.image_cover.image.url
        except AttributeError:
            return '/static/images/product-default-img.png'

    def get_images(self):
        return self.images.all()

    def get_attr_groups(self):
        if self.attr_category:
            return self.attr_category.get_groups()
        return []

    def get_orders(self):
        return Cart.objects.filter(invoice__purchase__isnull=False, productcart__product=self)


class ProductSold(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)
    product_selected = models.ForeignKey('ProductCart', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    count = models.IntegerField()
    details = models.TextField()

    def __str__(self):
        return f'{self.count} => {self.product_selected}'


class ProductInventory(BaseModel):
    product = models.OneToOneField('BasicProduct', on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f'{self.product} - {self.quantity}:{self.price}'


class ProductInventoryDefault(BaseModel):
    """
        TODO: should be Singleton Model
    """
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return f'settings {self.price} - {self.quantity} default product inventory'


class ProductAttrCategory(BaseModel):
    """
        Product Attribute Category
    """
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField('ProductAttrGroup', blank=True)

    def __str__(self):
        return self.name

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:product_attr_category__detail', args=(self.id,))

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

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:product_attr_group__detail', args=(self.id,))

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

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:product_attr_field__detail', args=(self.id,))

    def get_picture_url(self):
        try:
            return self.picture.url
        except ValueError:
            pass

    def get_groups(self):
        return self.productattrgroup_set.all()


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
    images = models.ManyToManyField('storage.Image')
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

    def get_invoice_purchase(self):
        try:
            return self.cart_item.cart.invoice.purchase
        except AttributeError:
            return None


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

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:category__detail', args=(self.id,))


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_products(self):
        return self.basicproduct_set.all()

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:tag__detail', args=(self.id,))


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


class DiscountCouponSelected(BaseModel):
    discount = models.ForeignKey('DiscountCoupon', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.discount}'


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
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=200)
    factor_code = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS, default='unseen')
    images = models.ManyToManyField('storage.Image', blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.user_name

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:factor_cake_image__detail', args=(self.id,))

    def get_images(self):
        return self.images.all()


def cart_tc_code():
    return utils.random_str(10)


class Cart(BaseModel):
    delivery_time = None

    # tc = models.CharField(max_length=14, default=cart_tc_code, unique=True) # TODO: use this when db is cleaned
    tc = models.CharField(max_length=14, default=cart_tc_code)
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)  # user or session cart in creation
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.user.__str__() or 'session cart'

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:order__detail', args=(self.id,))

    def get_absolute_url(self):
        return self.get_dashboard_absolute_url()

    def has_empty(self):
        return True if self.get_all_products_count() < 1 else False

    def has_products_in_stock(self):
        products_cart = self.get_products()
        for product_cart in products_cart:
            if product_cart.product.get_quantity() < product_cart.quantity:
                return False
        return True

    def has_custom_products(self):
        return False if self.get_custom_products().count() < 1 else True

    def get_products(self):
        return self.productcart_set.all()

    def get_custom_products(self):
        objs = self.customproductcart_set.all()
        if self.delivery_time and self.delivery_time == 'fastest':
            objs = objs.filter(custom_product__receipt_date__lte=str(now_shamsi_date()))
        return objs

    def get_custom_products_progress(self):
        return self.customproductcart_set.filter(custom_product__receipt_date__gt=str(now_shamsi_date()))

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
        return self.get_price()

    def get_price_paid(self):
        try:
            return self.invoice.purchase.price_paid
        except AttributeError:
            return None

    def get_invoice_purchase(self):
        try:
            return self.invoice.purchase
        except AttributeError:
            return None

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

    def products_sold(self, user):
        products = self.get_products()
        for product_cart in products:
            # decrease quantity
            product_inventory = product_cart.product.productinventory
            product_inventory.quantity -= product_cart.quantity
            product_inventory.save()
            # create sold object
            ProductSold.objects.create(
                user=user,
                product_selected=product_cart,
                count=product_cart.quantity,
                price=product_cart.product.get_price(),
                details=product_cart.get_detail()
            )


class CartStatus(BaseModel):
    STATUS_OPTIONS = (
        ('pending', _('Pending')),
        ('cancelled', _('Cancelled')),
        ('in_progress', _('In_progress')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
    )

    status = models.CharField(max_length=14, choices=STATUS_OPTIONS, default='pending')
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, related_name='status')

    def __str__(self):
        return f'{self.cart.tc} - {self.status}'


class ProductCart(BaseModel):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('BasicProduct', on_delete=models.SET_NULL, null=True)
    attrs_selected = models.ManyToManyField('ProductAttrSelected')
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.cart} - {self.product}'

    def get_attrs(self):
        return self.attrs_selected.all()

    def get_attrs_price(self):
        return self.get_attrs().aggregate(total=models.Sum('attr__additional_price'))['total'] or 0

    def get_total_price(self):
        return (self.product.get_price() + self.get_attrs_price()) * self.quantity

    def get_detail(self):
        return f"""
            cart_id: {self.cart.id}
            {self.product.title}(*{self.quantity})
            |
                {('{group_name}:{attr_name}'.format(group_name=attr.group.name, attr_name=attr.attr.name) for attr in self.get_attrs())}
            |
        """


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
