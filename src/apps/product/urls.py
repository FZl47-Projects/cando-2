from django.urls import path
from . import views

app_name = 'apps.product'
urlpatterns = [
    path('basic/list', views.BasicProductList.as_view(), name='basic_product__list'),
    path('basic/<int:product_id>/detail', views.BasicProductDetail.as_view(), name='basic_product__detail'),

    path('wishlist/<int:product_id>/add', views.WishListAdd.as_view(), name='wishlist__add'),

    path('comment/create', views.CommentCreate.as_view(), name='comment__create'),

    path('factor-cake-image', views.FactorCakeImage.as_view(), name='factor_cake_image__create'),
]
