from django.urls import path
from . import views

app_name = 'apps.product'
urlpatterns = [
    path('basic/list', views.BasicProductList.as_view(), name='basic_product__list'),
    path('basic/<int:product_id>/detail', views.BasicProductDetail.as_view(), name='basic_product__detail'),

    path('cart/product/<int:product_id>/create', views.ProductCartCreate.as_view(), name='product_cart__create'),

    path('wishlist/<int:product_id>/create', views.WishListProductCreate.as_view(), name='wishlist__create'),

    path('comment/create', views.CommentCreate.as_view(), name='comment__create'),

    path('factor-cake-image', views.FactorCakeImage.as_view(), name='factor_cake_image__create'),

    path('custom-product-create', views.CustomProductCreate.as_view(), name='custom_product__create'),
]
