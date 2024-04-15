from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View

from apps.core.utils import log_event, create_form_messages, get_host_url
from apps.product.models import Cart
from . import forms, models
from .gateways.zarinpal import Zarinpal


class InvoiceCreate(LoginRequiredMixin, View):
    form = forms.InvoiceCreateForm

    def post(self, request):
        data = request.POST
        cart_id = data['cart']
        cart_obj = get_object_or_404(Cart, id=cart_id)
        if not cart_obj.has_products_in_stock:
            messages.error(request, _('Products Not In Stock'))
            return self.request.META.get('HTTP_REFERER', '/')
        cart_invoice = getattr(cart_obj, 'invoice', None)
        if cart_invoice:
            return redirect(self.get_success_redirect_url(cart_invoice))
        f = self.form(data=data, files=request.FILES)
        if not f.is_valid():
            # create error message's
            create_form_messages(request, f)
            return redirect(self.get_fail_redirect_url())
        invoice = self.obj = f.save()
        return redirect(self.get_success_redirect_url(invoice))

    def get_success_redirect_url(self, invoice):
        return reverse('payment:invoice__purchase', args=(invoice.id,))

    def get_fail_redirect_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


class InvoicePurchase(LoginRequiredMixin, View):

    def get_call_back_url(self, invoice):
        return get_host_url(reverse('payment:invoice__purchase_callback', args=(invoice.id,)))

    def get(self, request, invoice_id):
        invoice = None
        try:
            invoice = models.Invoice.objects.get(id=invoice_id)
        except models.Invoice.DoesNotExist:
            pass
        #  manual invoice
        try:
            invoice = models.ManualInvoice.objects.get(id=invoice_id)
        except models.ManualInvoice.DoesNotExist:
            pass
        if not invoice:
            msg_err = 'There Is Some Problem In Fetch Invoice Or Manual Invoice Object'
            log_event(msg_err, 'ERROR')
            messages.error(request, _(msg_err))
            return redirect('public:cart')

        zp = Zarinpal()
        zp_status = zp.start_transaction(request, invoice.get_total_price(), self.get_call_back_url(invoice))
        if zp_status:
            return zp.redirect_to_gateway()
        return redirect('public:cart')


class InvoicePurchaseCallBack(LoginRequiredMixin, View):

    def get(self, request, invoice_id):
        invoice = None
        try:
            invoice = models.Invoice.objects.get(id=invoice_id)
            invoice.type = 'auto'
        except models.Invoice.DoesNotExist:
            pass

        #  manual invoice
        try:
            invoice = models.ManualInvoice.objects.get(id=invoice_id)
            invoice.type = 'manual'
        except models.ManualInvoice.DoesNotExist:
            pass

        if not invoice:
            messages.error(request, _('There Is Some Problem, Invoice Object DoesNotExist'))
            return redirect('public:cart')

        status = request.GET.get('Status')
        if status == 'NOK':
            messages.error(request, _('Cancel Request By User'))
            return redirect('public:cart')

        zp = Zarinpal()
        amount = invoice.get_total_price()
        zp_status = zp.verify_transaction(request, amount)
        if not zp_status:
            return redirect('public:cart')
        # payment success
        ref_id = zp.response['RefID']
        # create invoice payment
        purchase_invoice = models.PurchaseInvoice.objects.create(
            user=request.user,
            tracking_code=ref_id,
            bank_name='-',
            price_paid=amount
        )
        # set purchase object
        invoice.purchase = purchase_invoice
        invoice.save()

        cart = getattr(invoice, 'cart', None)
        if cart:
            custom_products_progress = cart.get_custom_products_progress()
            if custom_products_progress and invoice.delivery_time == 'fastest':
                # create and move custom products in progress other cart
                new_cart = Cart.objects.create(
                    user=request.user,
                )
                for custom_product in custom_products_progress:
                    custom_product.cart = new_cart
                    custom_product.save()
            # decrease product items
            cart.products_sold(request.user)
            # change status cart
            cart.is_active = False
            cart.save()

        messages.success(request, _('Payment Was Successful'))
        return redirect(invoice.get_absolute_url())
