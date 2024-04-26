from django.urls import path

from apps.dashboard.views.dashboard.shared import payment as views

urlpatterns = [
    # invoice
    path('invoice/list', views.InvoiceList.as_view(), name='invoice__list'),
    path('invoice/<int:invoice_id>/detail', views.InvoiceDetail.as_view(), name='invoice__detail'),
    path('invoice/<int:invoice_id>/detail/export', views.InvoiceDetailExport.as_view(),
         name='invoice__detail_export'),
    path('invoice/<int:invoice_id>/delete', views.InvoiceDelete.as_view(), name='invoice__delete'),
    # purchase invoice
    path('purchase-invoice/list', views.PurchaseInvoiceList.as_view(), name='purchase_invoice__list'),
    path('purchase-invoice/<int:purchase_invoice_id>/detail', views.PurchaseInvoiceDetail.as_view(),
         name='purchase_invoice__detail'),
    path('purchase-invoice/<int:purchase_invoice_id>/delete', views.PurchaseInvoiceDelete.as_view(),
         name='purchase_invoice__delete'),
]
