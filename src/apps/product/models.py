from django.shortcuts import reverse
from django.db import models
from apps.core.models import BaseModel


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


class Product(BaseModel):
    STATUS_OPTIONS = (
        ('active', 'فعال'),
        ('disable', 'غیر فعال'),
        ('archived', 'ارشیو'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveBigIntegerField(null=True, blank=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image_cover = models.ForeignKey('core.Image', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='product_cover')
    images = models.ManyToManyField('core.Image', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='active')

    objects = ProductManager()

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title

    def add_to_cart_url(self):
        # TODO: must be completed
        return ''

    def add_to_wishlist_url(self):
        # TODO: must be completed
        return ''

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('product:detail', args=(self.id,))

    def get_similar_products(self):
        return Product.objects.filter(categories__in=self.categories)

    def get_comments(self):
        return self.comment_set.filter(status='accepted')

    def get_all_comments(self):
        return self.comment_set.all()

    def get_rate(self):
        avg = self.get_comments().aggregate(rate_avg=models.Avg('rate'))['rate_avg'] or 0
        avg = round(avg, 1)
        return avg

    def get_image_cover(self):
        try:
            return self.image_cover.image.url
        except:
            # TODO: must be completed
            return '/static/images/logo.png'


class Category(BaseModel):
    title = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_products(self):
        return self.product_set.all()


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DiscountCoupon(BaseModel):
    code = models.CharField(max_length=30)
    price = models.PositiveBigIntegerField()
    expire_at = models.DateTimeField(null=True)
    count = models.PositiveBigIntegerField(null=True)
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
    STATUS_OPTIONS = (
        ('accepted', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('pending', 'در حال بررسی'),
    )

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.SmallIntegerField(choices=RATE_OPTIONS)
    status = models.CharField(max_length=15, choices=STATUS_OPTIONS)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'{self.title[:20]} - {self.product}'
