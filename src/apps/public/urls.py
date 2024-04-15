from django.urls import path
from . import views

app_name = 'apps.public'
urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('cart', views.Cart.as_view(), name='cart'),
    path('cart/checkout', views.CartCheckout.as_view(), name='checkout'),
]
