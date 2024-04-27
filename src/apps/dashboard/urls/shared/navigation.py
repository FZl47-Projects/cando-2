from django.urls import path

from apps.dashboard.views.dashboard.shared import navigation as views

urlpatterns = [
    path('address/default/manage', views.DefaultAddressManage.as_view(), name='address_default__manage'),
    path('address/create', views.AddressCreate.as_view(), name='address__create'),
    path('address/list', views.AddressList.as_view(), name='address__list'),
    path('address/<int:address_id>/detail', views.AddressDetail.as_view(), name='address__detail'),
    path('address/<int:address_id>/update', views.AddressUpdate.as_view(), name='address__update'),
]
