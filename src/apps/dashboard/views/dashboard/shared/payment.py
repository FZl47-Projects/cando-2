from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, View

from apps.core.auth import object_access
from apps.core.mixins.views import (
    FilterSimpleListViewMixin, DeleteViewMixin,
    UserRoleViewMixin, MultipleUserListViewMixin,
    MultipleUserViewMixin
)
from apps.payment import models


class InvoiceList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('cart__user__phonenumber__icontains', 'cart__tc__icontains', 'purchase__price_paid__icontains')
    filter_fields = ('purchase__isnull',)
    super_user_template = 'dashboard/admin/payment/invoice/list.html'
    user_template = 'dashboard/user/payment/invoice/list.html'

    def get_super_user_queryset(self):
        objects = models.Invoice.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_user_queryset(self):
        objects = self.request.user.get_invoices()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class InvoiceDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/payment/invoice/detail.html'
    user_template = 'dashboard/user/payment/invoice/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        invoice_id = kwargs['invoice_id']
        invoice = get_object_or_404(models.Invoice, id=invoice_id)
        cart = invoice.cart
        object_access(cart, self.request.user)
        context['invoice'] = invoice
        return context


class InvoiceDetailExport(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/payment/invoice/detail-export.html'
    user_template = 'dashboard/user/payment/invoice/detail-export.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        invoice_id = kwargs['invoice_id']
        invoice = get_object_or_404(models.Invoice, id=invoice_id)
        cart = invoice.cart
        object_access(cart, self.request.user)
        context['invoice'] = invoice
        context['export_type'] = self.request.GET.get('export_type', 'print')
        return context


class InvoiceDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:invoice__list')

    def get_object(self, request, *args, **kwargs):
        invoice_id = kwargs.get('invoice_id')
        return get_object_or_404(models.Invoice, id=invoice_id)


class PurchaseInvoiceList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = (
        'invoice__cart__user__phonenumber__icontains', 'invoice__cart__tc__icontains', 'price_paid__icontains')
    super_user_template = 'dashboard/admin/payment/invoice/purchase/list.html'
    user_template = 'dashboard/user/payment/invoice/purchase/list.html'

    def get_super_user_queryset(self):
        objects = models.PurchaseInvoice.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_user_queryset(self):
        objects = self.request.user.get_purchase_invoice()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class PurchaseInvoiceDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/payment/invoice/purchase/detail.html'
    user_template = 'dashboard/user/payment/invoice/purchase/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        purchase_invoice_id = kwargs['purchase_invoice_id']
        purchase_invoice = get_object_or_404(models.PurchaseInvoice, id=purchase_invoice_id)
        object_access(purchase_invoice, self.request.user)
        context['purchase_invoice'] = purchase_invoice
        return context


class PurchaseInvoiceDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:purchase_invoice__list')

    def get_object(self, request, *args, **kwargs):
        purchase_invoice_id = kwargs.get('purchase_invoice_id')
        return get_object_or_404(models.PurchaseInvoice, id=purchase_invoice_id)
