from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, View

from apps.core.mixins.views import (
    FilterSimpleListViewMixin, DeleteMixin,
)
from apps.payment import models


class InvoiceList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('cart__user__phonenumber__icontains', 'cart__tc__icontains', 'purchase__price_paid__icontains')
    filter_fields = ('purchase__isnull',)
    template_name = 'dashboard/admin/payment/invoice/list.html'

    def get_queryset(self):
        objects = models.Invoice.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context

    def filter(self, objects):
        objects = super().filter(objects)
        # advance filter
        purchase_status = self.request.GET.get('purchase')
        return objects


class InvoiceDetail(TemplateView):
    template_name = 'dashboard/admin/payment/invoice/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        invoice_id = kwargs['invoice_id']
        invoice = get_object_or_404(models.Invoice, id=invoice_id)
        context['invoice'] = invoice
        return context


class InvoiceDetailExport(TemplateView):
    template_name = 'dashboard/admin/payment/invoice/detail-export.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        invoice_id = kwargs['invoice_id']
        invoice = get_object_or_404(models.Invoice, id=invoice_id)
        context['invoice'] = invoice
        context['export_type'] = self.request.GET.get('export_type', 'print')
        return context


class InvoiceDelete(DeleteMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:invoice__list')

    def get_object(self, request, *args, **kwargs):
        invoice_id = kwargs.get('invoice_id')
        return get_object_or_404(models.Invoice, id=invoice_id)
