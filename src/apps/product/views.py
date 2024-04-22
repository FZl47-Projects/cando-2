from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View
from django.db.models import Min, Max, Count, Case, When, Value
from django.core.exceptions import PermissionDenied

from apps.core.mixins.views import CreateViewMixin, FilterSimpleListViewMixin, DeleteViewMixin
from apps.product import models, forms


class BasicProductList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    filter_fields = ('categories',)
    template_name = 'product/basic/list.html'

    def get_queryset(self):
        objects = models.BasicProduct.objects.get_active_list()
        return objects

    def get_context_data(self, **kwargs):
        """
            Order filter and lines is important
        """
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        context['total_count'] = products.count()
        context['min_price'] = products.aggregate(min_price=Min('productinventory__price'))['min_price']
        context['max_price'] = products.aggregate(max_price=Max('productinventory__price'))['max_price']
        # filter & sort
        products = self.search(products)
        products = self.filter(products)
        products = self.order_by(products)
        context['object_list'] = products
        context['categories'] = models.Category.objects.all()
        context['tags'] = models.Tag.objects.all()
        return context

    def filter(self, objects):
        objects = super().filter(objects)
        params = self.request.GET
        # advance filter
        # by price
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        if min_price:
            objects = objects.filter(productinventory__price__gte=min_price)
        if max_price:
            objects = objects.filter(productinventory__price__lte=max_price)

        return objects

    def order_by(self, objects):
        params = self.request.GET
        sort_by = params.get('sort_by')
        if sort_by:
            if sort_by == 'most_view':
                objects = objects.annotate(view_count=Count('productview')).order_by('-view_count')
            if sort_by == 'showcase':
                objects = objects.annotate(type_pr=Case(
                    When(type='showcase', then=Value(1)),
                    When(type='simple', then=Value(2)),
                    default=Value(2)
                )).order_by('type_pr')
            if sort_by == 'lowest_price':
                objects = objects.order_by('productinventory__price')
            if sort_by == 'highest_price':
                objects = objects.order_by('-productinventory__price')
            if sort_by == 'discount':
                # TODO: should be complete
                pass
            if sort_by == 'newest':
                objects = objects.order_by('-id')
            if sort_by == 'oldest':
                objects = objects.order_by('id')
        return objects


class BasicProductDetail(TemplateView):
    template_name = 'product/basic/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get('product_id')
        product = get_object_or_404(models.BasicProduct, id=product_id, status='active')
        context['product'] = product
        # create product view
        user = self.request.user
        models.ProductView.objects.create(product=product, user=None if user.is_authenticated is False else user)
        return context


class FactorCakeImage(CreateViewMixin, TemplateView):
    form = forms.FactorCakeImageCreateForm
    success_message = _('Your Cake Receipt Image Has Been Saved Successfully')
    # redirect_url = None => redirect to success page (redirect to referer for now)
    template_name = 'product/factor-cake-image.html'


class CustomProductCreate(CreateViewMixin, TemplateView):
    form = forms.CustomProductCreateForm
    success_message = _('Your Custom Product Has Been Created and Will Be Added to Your Shopping Cart After Checking')
    template_name = 'product/custom-product-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attr_category'] = models.CustomProductAttrCategory.objects.first()
        return context

    def add_additional_data(self, data):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied
        data['user'] = user


class CustomProductCartDelete(DeleteViewMixin, View):
    success_message = _('Product Cart Successfully Deleted')

    def get_object(self, request, *args, **kwargs):
        custom_product_cart_id = kwargs.get('custom_product_cart_id')
        custom_product_cart = get_object_or_404(models.CustomProductCart, id=custom_product_cart_id)
        # check cart user
        user = self.request.user
        if user.is_authenticated:
            cart = user.get_current_cart_or_create()
        else:
            cart = models.Cart.get_session_cart(self.request)
        if custom_product_cart.cart != cart:
            raise PermissionDenied
        return custom_product_cart


class CommentCreate(CreateViewMixin, View):
    form = forms.CommentCreateForm
    success_message = _('Your Comment Has Been Successfully Registered And Will Be Displayed After Review')

    def add_additional_data(self, data):
        # add user to data
        data['user'] = self.request.user


class ProductCartCreate(CreateViewMixin, View):
    form = forms.ProductCartCreateForm
    success_message = _('Product Has Been Successfully Added To The Cart')


class ProductCartDelete(DeleteViewMixin, View):
    success_message = _('Product Cart Successfully Deleted')

    def get_object(self, request, *args, **kwargs):
        product_cart_id = kwargs.get('product_cart_id')
        product_cart = get_object_or_404(models.ProductCart, id=product_cart_id)
        # check cart user
        user = self.request.user
        if user.is_authenticated:
            cart = user.get_current_cart_or_create()
        else:
            cart = models.Cart.get_session_cart(self.request)
        if product_cart.cart != cart:
            raise PermissionDenied
        return product_cart


class WishListProductCreate(View):
    success_message = _('Product Has Been Successfully Added To The Wish List')

    def get(self, request, product_id):
        product = get_object_or_404(models.BasicProduct, id=product_id)
        user = request.user
        if user.is_authenticated:
            wishlist = user.get_or_create_wishlist()
        else:
            wishlist = models.WishList.get_session_wishlist(request)
        wishlist.products.add(product)
        messages.success(request, self.success_message)
        # redirect to referer url
        referer_url = request.META.get('HTTP_REFERER')
        return redirect(referer_url or 'public:home')
