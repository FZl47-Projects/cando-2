from django.urls import path

from . import views

app_name = 'apps.payment'
urlpatterns = [
    path('invoice/create', views.InvoiceCreate.as_view(), name='invoice__create'),
    path('invoice/<int:invoice_id>/purchase', views.InvoicePurchase.as_view(), name='invoice__purchase'),
    path('invoice/<int:invoice_id>/purchase/callback', views.InvoicePurchaseCallBack.as_view(), name='invoice__purchase_callback'),
]
