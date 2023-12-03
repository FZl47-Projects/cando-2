import json, requests
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.conf import settings
from core.models import Image
from core.utils import form_validate_err, get_host_url
# from core.notify import send_sms
from core.auth.decorators import admin_required_cbv
from . import models, forms

User = get_user_model()


class CustomOrderProduct(LoginRequiredMixin, View):
    template_name = 'product/custom-order-product.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        images = request.FILES.getlist('image', [])
        image_objects = []
        for image in images:
            if image:
                img_obj = Image.objects.create(image=image)
                image_objects.append(img_obj)

        data = request.POST.copy()

        detail = {
            'taste_spongy': data.get('taste_spongy'),
            'taste_cream': data.get('taste_cream'),
            'filing_cake': data.get('filing_cake'),
            'type_order': data.get('type_order'),
            'date_receive': data.get('date_receive'),
            'hour': data.get('hour'),
            'minute': data.get('minute'),
            'amount_cream': data.get('amount_cream'),
            'weight': data.get('weight'),
            'writing_on_cake': data.get('writing_on_cake'),
            'description': data.get('description'),
        }
        description = data.get('description')
        custom_ord_product_obj = models.CustomOrderProduct.objects.create(
            user=request.user,
            detail=detail,
            description=description
        )
        custom_ord_product_obj.images.add(*image_objects)

        # send notif
        super_users = User.super_user.all()
        for user in super_users:
            send_sms('new_custom_order_registered', user.get_phonenumber())
        return redirect(f"{reverse('public:success')}?message=سفارش شما با موفقیت ثبت شد")


class CustomOrderProductFactorCreate(View):

    @admin_required_cbv
    def post(self, request, order_id):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        order_obj = get_object_or_404(models.CustomOrderProduct, id=order_id)
        cart = order_obj.user.get_or_create_cart()
        # set values
        data['cart'] = cart
        data['is_checked'] = True
        data['status'] = 'accepted'
        f = forms.CustomOrderProductAccept(data, instance=order_obj)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        # send notif
        send_sms('custom_order_estimated', order_obj.user.get_phonenumber(),
                 cart_link=get_host_url(reverse('product:cart')))
        messages.success(request, 'تخمین قیمت سفارش با موفقیت ثبت شد')
        return redirect(referer_url or '/success')


class CustomOrderProductReject(View):

    @admin_required_cbv
    def post(self, request, custom_order_id):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        # set values
        data['status'] = 'rejected'
        order_obj = get_object_or_404(models.CustomOrderProduct, id=custom_order_id)
        f = forms.CustomOrderProductReject(data, request.FILES, instance=order_obj)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        user = order_obj.user
        # send notif
        send_sms('custom_order_rejected', user.get_phonenumber(), user_name=user.get_full_name())
        messages.success(request, ' سفارش با موفقیت رد شد')
        return redirect(referer_url or '/success')


class Cart(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'product/cart.html')


class CartAdd(LoginRequiredMixin, View):

    def get(self, request, product_id):
        referer_url = request.META.get('HTTP_REFERER')
        product_obj = get_object_or_404(models.Product, id=product_id)
        cart = request.user.get_or_create_cart()
        # check product is stock
        if product_obj.is_in_stock is False:
            messages.error(request, 'محصول ناموجود میباشد')
            return redirect(referer_url or '/error')
        # check for duplicate product in cart
        if cart.get_orders().filter(product=product_obj).exists() is False:
            order_obj = models.Order.objects.create(
                cart=cart,
                product=product_obj,
                count=1
            )
        else:
            # product is duplicate
            pass
        messages.success(request, 'محصول به سبد خرید اضافه شد')
        return redirect(referer_url or '/success')


class CartRemoveOrder(LoginRequiredMixin, View):

    def get(self, request, order_id):
        referer_url = request.META.get('HTTP_REFERER')
        user = request.user
        order_obj = get_object_or_404(models.Order, id=order_id, cart__user=user)
        order_obj.delete()
        messages.success(request, 'محصول از سبد خرید حذف شد')
        return redirect(referer_url or '/success')


class CartRemoveCustomOrder(LoginRequiredMixin, View):

    def get(self, request, order_id):
        referer_url = request.META.get('HTTP_REFERER')
        user = request.user
        order_obj = get_object_or_404(models.CustomOrderProduct, id=order_id, cart__user=user)
        order_obj.delete()
        messages.success(request, 'محصول از سبد خرید حذف شد')
        return redirect(referer_url or '/success')


class CartProcessPayment(LoginRequiredMixin, View):

    def get(self, request):
        # check for active cart and have orders
        cart = request.user.get_current_cart(raise_err=True)
        if cart.have_orders is False:
            return redirect('product:cart')
        factor = getattr(cart, 'factor', None)
        if factor and factor.process_to_payment:
            factor.delete()
        context = {
            'settings': settings
        }
        return render(request, 'product/cart-process-payment.html', context)

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        user = request.user
        cart = user.get_current_cart()
        if cart is None:
            messages.error(request, 'سبد خرید فعالی یافت نشد')
            return redirect('product:cart')

        # TODO maybe need to refactor or change some structure in future
        orders_is_available = cart.orders_is_available
        # check cart have orders
        if cart.have_orders is False:
            messages.error(request, f"محصولی در سبد خرید شما یافت نشد")
            return redirect('product:cart')
        # orders_is_available is True or product name
        if orders_is_available is not True:
            messages.error(request, f" محصول {orders_is_available} ناموجود است ")
            return redirect('product:cart')

        # set values
        total_price = cart.get_total_price_for_payment()
        data['user'] = user
        data['cart'] = cart
        data['price'] = total_price
        data['shipping_fee'] = cart.get_shipping_fee()
        data['detail'] = cart.get_dict_detail_orders()
        delivery_type = data.get('delivery_type')
        if delivery_type == 'online':
            f = forms.FactorCreateForm(data)
        elif delivery_type == 'in-person':
            f = forms.FactorCreateNonAddressForm(data)
        else:
            return redirect(referer_url or '/error')
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        factor_obj = f.save()
        send_sms('factor_created', user.get_phonenumber(),
                 factor_link=get_host_url(factor_obj.get_payment_link()))
        return redirect(factor_obj.get_payment_link())


class FactorPayment(LoginRequiredMixin, View):

    def get(self, request, factor_id):
        factor_obj = get_object_or_404(models.Factor, id=factor_id, factorpayment=None)
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": factor_obj.get_price_rial(),
            "description": settings.ZP_DESCRIPTION,
            "phone": factor_obj.user.get_phonenumber(),
            "callback_url": get_host_url(reverse('product:factor_payment_verify')),
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                response_data = response.get('data', {})
                status_code_zp = response_data.get('code', 0)
                if status_code_zp == 100:
                    authority = str(response_data.get('authority'))
                    factor_obj.process_to_payment = True
                    factor_obj.save()
                    return redirect(settings.ZP_API_STARTPAY.format(authority=authority))
        except Exception as e:
            pass
        # if pay failed then delete factor
        # and for next payment create new factor
        factor_obj.delete()
        return redirect('public:error')


class FactorPaymentVerify(LoginRequiredMixin, View):

    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        user = request.user
        cart = user.get_current_cart(raise_err=True)
        factor = getattr(cart, 'factor', None)
        if factor is None:
            return redirect(reverse('public:error') + '?message=فاکتوری برای سبد خرید شما یافت نشد')
        if status != 'OK':
            # canceled by user
            factor.delete()
            return redirect(reverse('public:error') + '?message=درخواست توسط کاربر لغو شد')
        orders_is_available = cart.orders_is_available
        if orders_is_available is not True:
            messages.error(request, f" محصول {orders_is_available} ناموجود است ")
            return redirect('product:cart')
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": factor.get_price_rial(),
            "authority": authority
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)
        status_code = response.status_code
        if status_code != 200:
            return redirect(reverse('public:error') + '?message=مشکلی در عملیات پرداخت پیش امده است')
        response = response.json()
        response_data = response.get('data', {})
        status_code_zp = response_data.get('code', 0)
        if status_code_zp != 100:
            return redirect(reverse('public:error') + '?message=مشکلی در عملیات پرداخت پیش امده است')
        ref_id = response_data.get('ref_id', None)
        factor.process_to_payment = False
        factor.save()
        models.FactorPayment.objects.create(
            factor=factor,
            ref_id=ref_id,
            price_paid=factor.price
        )
        # update stock products
        cart.decrease_stock_products()
        cart.is_active = False
        cart.save()
        models.CartStatus.objects.create(
            cart=cart
        )
        messages.success(request, 'سفارش شما با موفقیت پرداخت و ثبت شد')
        send_sms('factor_paid', user.get_phonenumber(), ref_id=ref_id)
        # send notif
        super_users = User.super_user.all()
        for user in super_users:
            send_sms('new_order_paid_for_admin', user.get_phonenumber(), ref_id=ref_id)
        return redirect(cart.get_status_absolute_url())


class CartDetail(LoginRequiredMixin, View):

    def get(self, request, cart_id):
        user = request.user
        cart = get_object_or_404(models.Cart, id=cart_id, is_active=False)
        # only owner cart can access and admin
        if cart.user != user and user.is_admin is False:
            raise Http404
        context = {
            'cart': cart
        }
        return render(request, 'product/order-detail.html', context)


class CartStatus(View):

    def notify_cart_status(self, cart_obj, status_text):
        cart_user = cart_obj.user
        send_sms('cart_status', cart_user.get_phonenumber(), user_name=cart_user.name,
                 track_code=cart_obj.get_track_code(), status_text=status_text)

    @admin_required_cbv
    def post(self, request, cart_id):
        referer_url = request.META.get('HTTP_REFERER')
        cart_obj = get_object_or_404(models.Cart, id=cart_id)
        cart_status = cart_obj.cartstatus
        data = request.POST.copy()
        # set values
        data['cart'] = cart_obj
        f = forms.CartStatusForm(data, instance=cart_status)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        data = f.cleaned_data
        status = data.get('status')
        if status == 'accepted':
            self.notify_cart_status(cart_obj, 'تایید شد')
        elif status == 'send':
            self.notify_cart_status(cart_obj, 'در حال خروج از مرکز پردازش و ارسال سفارش است')
        messages.success(request, 'وضعیت سفارش با موفقیت بروز شد')
        return redirect(referer_url or '/success')


class FactorCakeImage(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'product/order-cake-image.html')


class FactorCakeImageSubmit(LoginRequiredMixin, View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        images = request.FILES.getlist('image', [])
        image_objects = []
        for image in images:
            if image:
                img_obj = Image.objects.create(image=image)
                image_objects.append(img_obj)

        f = forms.FactorCakeImageForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        factor_cake = f.save()
        factor_cake.images.add(*image_objects)
        return redirect(f"{reverse('public:success')}?message=عکس طرح کیک با موفقیت ثبت شد")


class ProductCreate(View):

    @admin_required_cbv
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST
        f = forms.ProductCreateForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'محصول با موفقیت ساخته شد')
        return redirect(referer_url or '/success')


class ProductUpdate(View):

    @admin_required_cbv
    def post(self, request, product_id):
        referer_url = request.META.get('HTTP_REFERER')
        product_obj = get_object_or_404(models.Product, id=product_id)
        data = request.POST
        f = forms.ProductUpdateForm(data, request.FILES, instance=product_obj)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'محصول با موفقیت بروزرسانی شد')
        return redirect(referer_url or '/success')


class ProductDelete(View):

    @admin_required_cbv
    def post(self, request, product_id):
        referer_url = request.META.get('HTTP_REFERER')
        product = get_object_or_404(models.Product, id=product_id)
        product.delete()
        messages.success(request, 'محصول با موفقیت حذف شد')
        return redirect(referer_url or '/success')


class CategoryCreate(View):

    @admin_required_cbv
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST
        f = forms.CategoryCreateForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'دسته بندی با موفقیت ساخته شد')
        return redirect(referer_url or '/success')


class CategoryDelete(View):

    @admin_required_cbv
    def post(self, request, category_id):
        referer_url = request.META.get('HTTP_REFERER')
        category = get_object_or_404(models.Category, id=category_id)
        category.delete()
        messages.success(request, 'دسته بندی با موفقیت حذف شد')
        return redirect(referer_url or '/success')


class ShowCaseCreate(View):

    @admin_required_cbv
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST
        product_ids = data.getlist('products', [])
        products_objs = models.Product.objects.filter(id__in=product_ids)
        showcase_obj = models.ShowCase.objects.first()
        if showcase_obj is None:
            showcase_obj = models.ShowCase.objects.create()
        showcase_obj.products.set(products_objs)
        messages.success(request, 'ویترین با موفقیت بروزرسانی شد')
        return redirect(referer_url or '/success')


class ProductFavoriteAdd(LoginRequiredMixin, View):

    def get(self, request, product_id):
        referer_url = request.META.get('HTTP_REFERER')
        product_obj = get_object_or_404(models.Product, id=product_id)
        user = request.user
        favorite_list = user.get_or_create_product_favorite_list()
        favorite_list.products.add(product_obj)
        messages.success(request, 'محصول با موفقیت به لیست مورد علاقه های شما اضافه شد')
        return redirect(referer_url or '/success')


class ProductFavoriteRemove(LoginRequiredMixin, View):

    def get(self, request, product_id):
        referer_url = request.META.get('HTTP_REFERER')
        product_obj = get_object_or_404(models.Product, id=product_id)
        user = request.user
        favorite_list = user.get_or_create_product_favorite_list()
        favorite_list.products.remove(product_obj)
        messages.success(request, 'محصول با موفقیت از لیست مورد علاقه های شما حذف شد')
        return redirect(referer_url or '/success')


class ProductDetail(View):

    def get(self, request, product_id):
        product_obj = get_object_or_404(models.Product, id=product_id)
        context = {
            'product': product_obj
        }
        return render(request, 'product/detail.html', context)


class CommentAdd(LoginRequiredMixin, View):

    def post(self, request, product_id):
        referer_url = request.META.get('HTTP_REFERER')
        product_obj = get_object_or_404(models.Product, id=product_id)
        data = request.POST.copy()
        # set values
        data['product'] = product_obj
        data['user'] = request.user
        f = forms.CommentAddForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'نظر شما با موفقیت ثبت شد پس از بررسی نمایش داده میشود')
        return redirect(referer_url or '/success')


class CommentAccept(View):

    @admin_required_cbv
    def get(self, request, comment_id):
        referer_url = request.META.get('HTTP_REFERER')
        comment_obj = get_object_or_404(models.Comment, id=comment_id)
        comment_obj.is_accepted = True
        comment_obj.save()
        messages.success(request, 'نظر با موفقیت تایید شد')
        return redirect(referer_url or '/success')


class CommentDelete(View):

    @admin_required_cbv
    def get(self, request, comment_id):
        referer_url = request.META.get('HTTP_REFERER')
        comment_obj = get_object_or_404(models.Comment, id=comment_id)
        comment_obj.delete()
        messages.success(request, 'نظر با موفقیت حذف شد')
        return redirect(referer_url or '/success')
