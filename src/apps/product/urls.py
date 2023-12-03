from django.urls import path
from . import views

app_name = 'apps.product'
urlpatterns = [
    path('custom-order-product', views.CustomOrderProduct.as_view(), name='custom_order_product'),
    path('custom-order-product/<int:order_id>/factor/create', views.CustomOrderProductFactorCreate.as_view(),
         name='custom_order_factor_create'),
    path('custom-order-product/<int:custom_order_id>', views.CustomOrderProductReject.as_view(),
         name='custom_order_reject'),

    path('factor-cake-image', views.FactorCakeImage.as_view(), name='factor_cake_image'),
    path('factor-cake-image/submit', views.FactorCakeImageSubmit.as_view(), name='factor_cake_image_submit'),

    path('create', views.ProductCreate.as_view(), name='create'),
    path('detail/<int:product_id>', views.ProductDetail.as_view(), name='detail'),
    path('update/<int:product_id>', views.ProductUpdate.as_view(), name='update'),
    path('delete/<int:product_id>', views.ProductDelete.as_view(), name='delete'),

    path('category/create', views.CategoryCreate.as_view(), name='category_create'),
    path('category/delete/<int:category_id>', views.CategoryDelete.as_view(), name='category_delete'),

    path('showcase/create', views.ShowCaseCreate.as_view(), name='showcase_create'),

    path('cart', views.Cart.as_view(), name='cart'),
    path('cart/add/<int:product_id>', views.CartAdd.as_view(), name='cart_add'),
    path('cart/remove/order/<int:order_id>', views.CartRemoveOrder.as_view(), name='cart_remove_order'),
    path('cart/remove/custom-order/<int:order_id>', views.CartRemoveCustomOrder.as_view(),
         name='cart_remove_custom_order'),
    path('cart/process-payment', views.CartProcessPayment.as_view(), name='cart_process_payment'),
    path('cart/payment/<int:factor_id>', views.FactorPayment.as_view(), name='factor_payment'),
    path('cart/payment/verify', views.FactorPaymentVerify.as_view(), name='factor_payment_verify'),
    path('cart/<int:cart_id>', views.CartDetail.as_view(), name='cart_detail'),
    path('cart/<int:cart_id>/status', views.CartStatus.as_view(), name='cart_status'),

    path('favorite/<int:product_id>/add', views.ProductFavoriteAdd.as_view(), name='favorite_add'),
    path('favorite/<int:product_id>/remove', views.ProductFavoriteRemove.as_view(), name='favorite_remove'),

    path('comment/<int:product_id>/add', views.CommentAdd.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/accept', views.CommentAccept.as_view(), name='comment_accept'),
    path('comment/<int:comment_id>/delete', views.CommentDelete.as_view(), name='comment_delete'),
]
