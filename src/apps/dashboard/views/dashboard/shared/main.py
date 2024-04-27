import json
import datetime
from django.views.generic import TemplateView
from django.db.models import Sum, F, Count, Q

from apps.core.utils import get_time
from apps.core.mixins.views import MultipleUserViewMixin

from apps.account.models import User
from apps.payment.models import PurchaseInvoice, Invoice
from apps.product.models import Cart, FactorCakeImage, CustomProduct, Comment


class Index(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/index.html'
    user_template = 'dashboard/user/index.html'

    def add_purchase_detail(self, context):
        # (purchase & payment)
        time_now = get_time(None)
        purchase = PurchaseInvoice.objects.all()
        # purchase time range
        last_month_purchase_date__min = time_now - datetime.timedelta(days=30)
        previous_month_purchase_date__min = time_now - datetime.timedelta(days=60)
        # last month
        last_month_purchase = purchase.filter(created_at__gte=last_month_purchase_date__min)
        last_month_total_purchase = last_month_purchase.aggregate(total=Sum('price_paid'))['total'] or 0
        last_month_purchase.total = last_month_total_purchase
        purchase_date_chart__range = last_month_purchase.values('created_at__day').annotate(
            day=F('created_at__day'), total_amount=Sum('price_paid'))
        purchase_date_chart__range = list(purchase_date_chart__range)
        last_month_purchase.chart_range = json.dumps(purchase_date_chart__range)
        # previous month
        previous_month_purchase = purchase.filter(created_at__lt=last_month_purchase_date__min,
                                                  created_at__gte=previous_month_purchase_date__min)
        previous_month_total_purchase = previous_month_purchase.aggregate(total=Sum('price_paid'))['total'] or 1

        # calculate the percentage of positive or negative
        last_month_purchase.percentage = (((
                                                   last_month_total_purchase - previous_month_total_purchase) // previous_month_total_purchase) * 100)
        context['purchase'] = last_month_purchase

    def add_order_detail(self, context):
        # (order)
        time_now = get_time(None)
        orders = Cart.objects.exclude(invoice__purchase=None)
        last_year_date__min = time_now - datetime.timedelta(days=365)
        orders = orders.filter(created_at__gte=last_year_date__min)
        order_date_chart__range = orders.values('created_at__month').annotate(
            month=F('created_at__month'), total=Count('id'))
        order_date_chart__range = list(order_date_chart__range)
        orders.chart_range = json.dumps(order_date_chart__range)
        context['orders'] = orders

    def add_user_detail(self, context):
        # (user)
        # sort by loyal users (most purchases)
        users = User.normal_user_objects.all().annotate(
            total_order=Count('cart', filter=~Q(cart__invoice__purchase=None))).order_by('-total_order')
        context['users'] = users
        context['admins'] = User.super_user_objects.all()

    def add_invoice_detail(self, context):
        # (invoice)
        invoices = Invoice.objects.all()
        invoices.need_to_pay = invoices.filter(purchase=None)
        invoices.paid = invoices.exclude(purchase=None)
        context['invoices'] = invoices

    def get_super_user_context(self):
        context = {
            'factor_cake_images': FactorCakeImage.objects.all(),
            'custom_products': CustomProduct.objects.all(),
            'comments': Comment.objects.all()
        }

        self.add_purchase_detail(context)
        self.add_order_detail(context)
        self.add_user_detail(context)
        self.add_invoice_detail(context)

        return context
