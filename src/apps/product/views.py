from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View
from django.db.models import Min, Max, Count, Case, When, Value, Sum

from apps.core.mixins.views import CreateViewMixin, FilterSimpleListViewMixin
from apps.core.utils import create_form_messages
from apps.product import models, forms, utils


class BasicProductList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    filter_fields = ('categories',)
    template_name = 'product/basic/list.html'

    def get_queryset(self):
        objects = models.BasicProduct.objects.all()
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
        product = get_object_or_404(models.BasicProduct, id=product_id)
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

    def do_success(self):
        # TODO: create notify for admins
        pass


class CustomProductCreate(CreateViewMixin, TemplateView):
    form = forms.CustomProductCreateForm
    success_message = _('Your Custom Product Has Been Created and Will Be Added to Your Shopping Cart After Checking')
    template_name = 'product/custom-product-create.html'

    def do_success(self):
        # TODO: create notify for admins and user
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attr_category'] = models.CustomProductAttrCategory.objects.first()
        return context


class CommentCreate(CreateViewMixin, View):
    form = forms.CommentCreateForm
    success_message = _('Your Comment Has Been Successfully Registered And Will Be Displayed After Review')

    def add_additional_data(self, data):
        # add user to data
        data['user'] = self.request.user

    def do_success(self):
        # TODO: create notify for admins
        pass


class ProductCartCreate(View):
    # TODO: should test
    success_message = _('Product Has Been Successfully Added To The Cart')

    def get_product(self):
        request = self.request
        data = request.POST
        product_id = data.get('product_id')
        product = get_object_or_404(models.BasicProduct, id=product_id)
        return product

    def get_request_data(self):
        req = self.request
        if req.method == 'GET':
            return req.GET.copy()
        elif req.method == 'POST':
            return req.POST.copy()
        # invalid method
        return redirect('public:home')

    def create_product_cart(self, cart, product):
        request = self.request
        data = self.get_request_data()
        data.update({
            'cart': cart.id,
            'product': product,
        })
        f = forms.ProductCartCreateForm(data=data)
        if not f.is_valid():
            create_form_messages(request, f)
            return
        product_cart = f.save()
        return product_cart

    def create_product_options_cart(self, product_cart):
        # TODO: should test and complete
        data = self.get_request_data()
        data.update({
            'product_cart': product_cart.id
        })
        f = forms.ProductOptionsCartCreateForm(data=data)
        if f.is_valid():
            f.save()

    def get_referer_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def check_stock_product_in_cart(self, product, cart):
        product_cart = cart.productcart_set.filter(product=product, cart=cart)
        if product_cart.exists():
            product_cart_quantities = product_cart.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            data = self.get_request_data()
            quantity = int(data['quantity'])
            if (product_cart_quantities + quantity) > product.get_quantity():
                return False
        return True

    def post(self, request, product_id):
        user = request.user
        if user.is_authenticated:
            cart = user.get_current_cart_or_create()
        else:
            cart = models.Cart.get_session_cart(request)
        product = get_object_or_404(models.BasicProduct, id=product_id)
        # check product stock and (stock cart)
        if (not product.has_in_stock()) or (not self.check_stock_product_in_cart(product, cart)):
            messages.warning(request, _('There Are Too Many Products In Your Shopping Cart'))
            return redirect(self.get_referer_url())
        product_cart = self.create_product_cart(cart, product)
        if not product_cart:
            return redirect(self.get_referer_url())
        self.create_product_options_cart(product_cart)
        messages.success(request, self.success_message)
        # redirect to referer url
        return redirect(self.get_referer_url())


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
