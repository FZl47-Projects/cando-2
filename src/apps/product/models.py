from jsonfield import JSONField
from django.shortcuts import reverse
from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.core.utils import random_str


def upload_src(instance, path):
    frmt = str(path).split('.')[-1]
    return f'product/images/{random_str(20)}.{frmt}'


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveBigIntegerField()
    stock = models.PositiveIntegerField(default=1)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_src, max_length=400)

    class Meta:
        ordering = '-id',

    @property
    def is_in_stock(self):
        return True if self.stock > 0 else False

    def __str__(self):
        return self.name

    def get_image_url(self):
        try:
            return self.image.url
        except:
            # default image
            # TODO: should be completed
            return ''

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('product:detail', args=(self.id,))

    def get_similar_products(self):
        return Product.objects.filter(category=self.category)

    def get_comments(self):
        return self.comment_set.filter(is_accepted=True)

    def get_all_comments(self):
        return self.comment_set.all()

    def get_rate(self):
        avg = self.get_comments().aggregate(rate_avg=models.Avg('rate'))['rate_avg'] or 0
        avg = round(avg, 1)
        return avg


class Category(BaseModel):
    type_name = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_products(self):
        return self.product_set.all()


class FactorCakeImage(BaseModel):
    user_name = models.CharField(max_length=200)
    track_code = models.CharField(max_length=100)
    description = models.TextField(null=True)
    images = models.ManyToManyField('core.Image')
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.user_name

    def get_images(self):
        return self.images.all()


class ShowCase(BaseModel):
    """
        Singleton Model
    """
    products = models.ManyToManyField('Product')

    def __str__(self):
        return 'show case'

    def get_products(self):
        return self.products.all()

    def save(self, *args, **kwargs):
        if ShowCase.objects.count() > 0:
            ShowCase.objects.all().delete()
        super(ShowCase, self).save(*args, **kwargs)


class Cart(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    discount = models.ForeignKey('Discount', null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} cart - {self.user}'

    @property
    def orders_is_available(self):
        orders = self.get_orders()
        for order in orders:
            if order.product.stock < order.count:
                return order.product.name
        return True

    @property
    def have_orders(self):
        orders = self.get_orders()
        custom_orders = self.get_custom_orders()
        if orders.count() == 0 and custom_orders.count() == 0:
            return False
        return True

    def get_orders(self):
        return self.order_set.all()

    def get_custom_orders(self):
        return self.customorderproduct_set.all()

    def get_total_price(self):
        return self.get_orders_price() + self.get_custom_orders_price()

    def get_total_price_for_payment(self):
        """
            calculate discount and shipping price or ..
        """
        cart_total = self.get_total_price()
        fee = self.get_shipping_fee()
        total = cart_total + fee
        return total

    def get_shipping_fee(self):
        tp_conf = settings.TRANSPORTATION_CONFIG
        fee = tp_conf['fee']
        if self.get_total_price() > tp_conf['free_if_price_more_than']:
            fee = 0
        return fee

    def get_orders_price(self):
        return self.get_orders().aggregate(p=models.Sum(
            models.F('product__price') * models.F('count')
        )
        )['p'] or 0

    def get_custom_orders_price(self):
        return self.get_custom_orders().aggregate(p=models.Sum('price'))['p'] or 0

    def get_dict_detail_orders(self):
        orders = []
        # orders
        [orders.append(order.get_dict_detail()) for order in self.get_orders()]
        # custom orders
        [orders.append(order.get_dict_detail()) for order in self.get_custom_orders()]
        return {
            'orders': orders
        }

    def get_track_code(self):
        try:
            return self.factor.track_code
        except:
            return 'چیزی یافت نشد'

    def get_receiver_user_info(self):
        address = self.factor.address
        return f'{address.receiver_phonenumber} - {address.receiver_name}'

    def decrease_stock_products(self):
        orders = self.get_orders()
        for order in orders:
            product = order.product
            product.stock -= order.count
            product.save()

    def get_absolute_url(self):
        return reverse('product:cart_detail', args=(self.id,))

    def get_time_submited(self):
        try:
            return self.factor.factorpayment.get_created_at()
        except:
            return 'ثبت نشده است'

    def get_timepast_submited(self):
        try:
            return self.factor.factorpayment.get_created_at_timepast()
        except:
            return ''


class CartStatus(BaseModel):
    STATUS_OPTIONS = (
        ('checking', 'در حال بررسی'),
        ('accepted', 'تایید'),
        ('send', 'خروج از مرکز سفارش'),
        ('delivered', 'تحویل به مشتری'),
    )
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='checking')
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE)
    delivery_time = models.IntegerField(null=True)  # approximate delivery time by minute

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'{self.cart} - {self.status}'

    def get_status_label(self):
        return self.get_status_display()


class Order(BaseModel):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f'#{self.id} order - {self.product} - {self.cart.user}'

    def get_total_price(self):
        return self.product.price * self.count

    def get_dict_detail(self):
        return {
            'product': self.product.name,
            'product_price': self.product.get_price(),
            'product_image': self.product.get_image_url(),
            'product_category': self.product.category.name,
            'count': self.count
        }

    @property
    def product_is_available(self):
        return self.product.stock >= self.count and self.product.stock > 0


class CustomOrderProduct(BaseModel):
    STATUS_OPTIONS = (
        ('accepted', 'تایید شد'),
        ('pending', 'در حال بررسی'),
        ('rejected', 'رد شد')
    )
    status = models.CharField(max_length=15, choices=STATUS_OPTIONS, default='pending')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    detail = JSONField()
    description = models.TextField(null=True)
    images = models.ManyToManyField('core.Image')
    # complete by admin
    note = models.TextField(null=True)
    is_checked = models.BooleanField(default=False)
    cart = models.ForeignKey('Cart', null=True, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} custom order product'

    def get_images(self):
        return self.images.all()

    def get_image_cover(self):
        return self.get_images().first()

    def get_dict_detail(self):
        return {
            'product': 'سفارش دلخواه',
            'product_price': self.price,
            'product_image': self.get_image_cover(),
            'product_category': 'دسته بندی سفارش دلخواه',
            'count': 1
        }


class Factor(BaseModel):
    DELIVERY_TYPE_OPTIONS = (
        ('online', 'online'),
        ('in-person', 'in-person'),
    )

    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE)
    track_code = models.CharField(default=random_str, max_length=20)
    price = models.PositiveBigIntegerField()
    shipping_fee = models.PositiveBigIntegerField(default=0)
    detail = JSONField()
    note = models.TextField(null=True)
    # address = models.ForeignKey('transportation.Address', null=True, on_delete=models.SET_NULL)
    delivery_type = models.CharField(choices=DELIVERY_TYPE_OPTIONS, max_length=10)
    process_to_payment = models.BooleanField(default=False)  # True if processing to payment(redirected to bank portal)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.track_code

    def get_payment_link(self):
        return reverse('product:factor_payment', args=(self.id,))

    def get_price_rial(self):
        return self.price * 10

    @classmethod
    def create(cls, factor, user):
        if factor.process_to_payment:
            return cls.objects.create(
                user=user, factor=factor, price=factor.price
            )


class FactorPayment(BaseModel):
    factor = models.OneToOneField('Factor', on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=50)
    detail = models.TextField(null=True)
    price_paid = models.PositiveBigIntegerField()

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} factor payment'


class Discount(BaseModel):
    code = models.CharField(max_length=30)
    price = models.PositiveBigIntegerField()
    expire_at = models.DateTimeField(null=True)
    cart_price_more = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.code


class ProductFavoriteList(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')

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

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.SmallIntegerField(choices=RATE_OPTIONS)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'{self.title[:20]} - {self.product}'


class CandyBox(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='user_boxes')
    weight = models.PositiveIntegerField('Weight', default=2)

    class Meta:
        ordering = '-id',


class Candy(BaseModel):
    name = models.CharField('Name', max_length=200)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class BoxRow(BaseModel):
    box = models.ForeignKey('CandyBox', on_delete=models.CASCADE, related_name='box_rows')
    candy = models.ForeignKey('Candy', on_delete=models.PROTECT, related_name='candy_rows')

    class Meta:
        ordering = '-id',


class Pakage(BaseModel):
    name = models.CharField('Name', max_length=200)
    price = models.IntegerField('Price', default=0)
    balloon = models.BooleanField(default=False)
    candle = models.BooleanField(default=False)
    thread = models.BooleanField(default=False)
    dish = models.BooleanField(default=False)
    images = models.ManyToManyField('core.Image')

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name
