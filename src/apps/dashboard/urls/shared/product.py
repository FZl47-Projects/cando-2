from django.urls import path
from apps.dashboard.views.dashboard.shared import product as views

urlpatterns = [
    # order
    path('order/list', views.OrderList.as_view(), name='order__list'),
    path('order/<int:order_id>/detail', views.OrderDetail.as_view(), name='order__detail'),
    path('order/<int:order_id>/delete', views.OrderDelete.as_view(), name='order__delete'),
    path('order/<int:order_status_id>/manage/status', views.OrderManageStatus.as_view(),
         name='order__manage_status'),
    path('product/basic/create', views.BasicProductCreate.as_view(), name='basic_product__create'),
    path('product/basic/list', views.BasicProductList.as_view(), name='basic_product__list'),
    path('product/basic/<int:product_id>/detail', views.BasicProductDetail.as_view(),
         name='basic_product__detail'),
    path('product/basic/<int:product_id>/update', views.BasicProductUpdate.as_view(),
         name='basic_product__update'),
    path('product/basic/<int:product_id>/images/update', views.BasicProductImagesUpdate.as_view(),
         name='basic_product_images__update'),
    path('product/basic/<int:product_id>/delete', views.BasicProductDelete.as_view(),
         name='basic_product__delete'),

    path('product/inventory/<int:inventory_id>/update', views.ProductInventoryUpdate.as_view(),
         name='product_inventory__update'),

    path('custom-product/list', views.CustomProductList.as_view(), name='custom_product__list'),
    path('custom-product/<int:custom_product_id>/detail', views.CustomProductDetail.as_view(),
         name='custom_product__detail'),
    path('custom-product/<int:custom_product_id>/delete', views.CustomProductDelete.as_view(),
         name='custom_product__delete'),
    path('custom-product/<int:custom_product_id>/status/manage', views.CustomProductManageStatus.as_view(),
         name='custom_product__manage_status'),

    # settings
    # product attributes section
    path('settings/custom-product/attr/field/category', views.CustomProductAttrCategoryManage.as_view(),
         name='custom_product_attr_category__manage'),

    # attr category
    path('settings/product/attr/category/create', views.ProductAttrCategoryCreate.as_view(),
         name='product_attr_category__create'),
    path('settings/product/attr/category/list', views.ProductAttrCategoryList.as_view(),
         name='product_attr_category__list'),
    path('settings/product/attr/category/<int:category_id>/detail', views.ProductAttrCategoryDetail.as_view(),
         name='product_attr_category__detail'),
    path('settings/product/attr/category/<int:category_id>/update', views.ProductAttrCategoryUpdate.as_view(),
         name='product_attr_category__update'),
    path('settings/product/attr/category/<int:category_id>/delete', views.ProductAttrCategoryDelete.as_view(),
         name='product_attr_category__delete'),

    # attr group
    path('settings/product/attr/group/create', views.ProductAttrGroupCreate.as_view(),
         name='product_attr_group__create'),
    path('settings/product/attr/group/list', views.ProductAttrGroupList.as_view(),
         name='product_attr_group__list'),
    path('settings/product/attr/group/<int:group_id>/detail', views.ProductAttrGroupDetail.as_view(),
         name='product_attr_group__detail'),
    path('settings/product/attr/group/<int:group_id>/update', views.ProductAttrGroupUpdate.as_view(),
         name='product_attr_group__update'),
    path('settings/product/attr/group/<int:group_id>/delete', views.ProductAttrGroupDelete.as_view(),
         name='product_attr_group__delete'),

    # attr field
    path('settings/product/attr/field/create', views.ProductAttrFieldCreate.as_view(),
         name='product_attr_field__create'),
    path('settings/product/attr/field/list', views.ProductAttrFieldList.as_view(),
         name='product_attr_field__list'),
    path('settings/product/attr/field/<int:field_id>/detail', views.ProductAttrFieldDetail.as_view(),
         name='product_attr_field__detail'),
    path('settings/product/attr/field/<int:field_id>/update', views.ProductAttrFieldUpdate.as_view(),
         name='product_attr_field__update'),
    path('settings/product/attr/field/<int:field_id>/delete', views.ProductAttrFieldDelete.as_view(),
         name='product_attr_field__delete'),

    # product inventory
    path('settings/product/inventory/manage', views.ProductInventoryDefaultManage.as_view(),
         name='inventory_default__manage'),

    # comment
    path('product/comment/list', views.CommentList.as_view(), name='comment__list'),
    path('product/comment/<int:comment_id>/detail', views.CommentDetail.as_view(), name='comment__detail'),
    path('product/comment/<int:comment_id>/delete', views.CommentDelete.as_view(), name='comment__delete'),
    path('product/comment/manage/status', views.CommentManageStatus.as_view(), name='comment__manage_status'),
    # category
    path('product/category/create', views.CategoryCreate.as_view(), name='category__create'),
    path('product/category/list', views.CategoryList.as_view(), name='category__list'),
    path('product/category/<int:category_id>/detail', views.CategoryDetail.as_view(), name='category__detail'),
    path('product/category/<int:category_id>/update', views.CategoryUpdate.as_view(), name='category__update'),
    path('product/category/<int:category_id>/delete', views.CategoryDelete.as_view(), name='category__delete'),
    # tag
    path('product/tag/create', views.TagCreate.as_view(), name='tag__create'),
    path('product/tag/list', views.TagList.as_view(), name='tag__list'),
    path('product/tag/<int:tag_id>/detail', views.TagDetail.as_view(), name='tag__detail'),
    path('product/tag/<int:tag_id>/delete', views.TagDelete.as_view(), name='tag__delete'),
    # discount
    # discount coupon
    path('product/discount/coupon/create', views.DiscountCouponCreate.as_view(),
         name='discount_coupon__create'),
    path('product/discount/coupon/list', views.DiscountCouponList.as_view(), name='discount_coupon__list'),
    # factor cake image
    path('product/factor-cake-image/list', views.FactorCakeImageList.as_view(), name='factor_cake_image__list'),
    path('product/factor-cake-image/<int:factor_cake_image_id>/detail', views.FactorCakeImageDetail.as_view(),
         name='factor_cake_image__detail'),
    path('product/factor-cake-image/<int:factor_cake_image_id>/delete', views.FactorCakeImageDelete.as_view(),
         name='factor_cake_image__delete'),
]
