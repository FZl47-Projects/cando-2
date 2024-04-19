from django.urls import path
from . import views

app_name = 'apps.dashboard'
urlpatterns = [
    # main
    path('', views.Index.as_view(), name='index'),
    # product
    path('order/list', views.product.OrderList.as_view(), name='order__list'),
    path('order/<int:order_id>/detail', views.product.OrderDetail.as_view(), name='order__detail'),
    path('order/<int:order_id>/delete', views.product.OrderDelete.as_view(), name='order__delete'),
    path('order/<int:order_status_id>/manage/status', views.product.OrderManageStatus.as_view(),
         name='order__manage_status'),

    path('product/basic/create', views.product.BasicProductCreate.as_view(), name='basic_product__create'),
    path('product/basic/list', views.product.BasicProductList.as_view(), name='basic_product__list'),
    path('product/basic/<int:product_id>/detail', views.product.BasicProductDetail.as_view(),
         name='basic_product__detail'),
    path('custom-product/list', views.product.CustomProductList.as_view(), name='custom_product__list'),
    path('custom-product/<int:custom_product_id>/detail', views.product.CustomProductDetail.as_view(),
         name='custom_product__detail'),
    path('custom-product/<int:custom_product_id>/delete', views.product.CustomProductDelete.as_view(),
         name='custom_product__delete'),
    path('custom-product/<int:custom_product_id>/status/manage', views.product.CustomProductManageStatus.as_view(),
         name='custom_product__manage_status'),
    path('custom-product/attr/field/category', views.product.CustomProductAttrCategoryManage.as_view(),
         name='custom_product_attr_category__manage'),
    # product attributes section
    # attr category
    path('product/attr/category/list', views.product.ProductAttrCategoryList.as_view(),
         name='product_attr_category__list'),
    path('product/attr/category/create', views.product.ProductAttrCategoryCreate.as_view(),
         name='product_attr_category__create'),
    # attr group
    path('product/attr/group/list', views.product.ProductAttrGroupList.as_view(), name='product_attr_group__list'),
    path('product/attr/group/create', views.product.ProductAttrGroupCreate.as_view(),
         name='product_attr_group__create'),
    # attr field
    path('product/attr/field/list', views.product.ProductAttrFieldList.as_view(), name='product_attr_field__list'),
    path('product/attr/field/create', views.product.ProductAttrFieldCreate.as_view(),
         name='product_attr_field__create'),
    # comment
    path('product/comment/list', views.product.CommentList.as_view(), name='comment__list'),
    path('product/comment/<int:comment_id>/detail', views.product.CommentDetail.as_view(), name='comment__detail'),
    path('product/comment/<int:comment_id>/delete', views.product.CommentDelete.as_view(), name='comment__delete'),
    path('product/comment/manage/status', views.product.CommentManageStatus.as_view(), name='comment__manage_status'),
    # category
    path('product/category/create', views.product.CategoryCreate.as_view(), name='category__create'),
    path('product/category/list', views.product.CategoryList.as_view(), name='category__list'),
    # tag
    path('product/tag/create', views.product.TagCreate.as_view(), name='tag__create'),
    path('product/tag/list', views.product.TagList.as_view(), name='tag__list'),
    # discount
    # discount coupon
    path('product/discount/coupon/create', views.product.DiscountCouponCreate.as_view(),
         name='discount_coupon__create'),
    path('product/discount/coupon/list', views.product.DiscountCouponList.as_view(), name='discount_coupon__list'),
    # factor cake image
    path('product/factor-cake-image/list', views.product.FactorCakeImageList.as_view(), name='factor_cake_image__list'),
    path('product/factor-cake-image/<int:factor_cake_image_id>/detail', views.product.FactorCakeImageDetail.as_view(),
         name='factor_cake_image__detail'),
    path('product/factor-cake-image/<int:factor_cake_image_id>/delete', views.product.FactorCakeImageDelete.as_view(),
         name='factor_cake_image__delete'),
    # user
    path('user/list', views.account.UserList.as_view(), name='user__list'),

    # storage
    path('storage/gallery/list', views.storage.GalleryImageList.as_view(), name='gallery__list'),
    path('storage/gallery/<int:image_id>/delete', views.storage.GalleryImageDelete.as_view(), name='gallery__delete'),

]
