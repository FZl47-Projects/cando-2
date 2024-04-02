from django.urls import path
from . import views

app_name = 'apps.dashboard'
urlpatterns = [
    # main
    path('', views.Index.as_view(), name='index'),
    # product
    path('product/basic/create', views.product.BasicProductCreate.as_view(), name='basic_product__create'),
    path('product/basic/list', views.product.BasicProductList.as_view(), name='basic_product__list'),
    path('product/basic/<int:product_id>/detail', views.product.BasicProductDetail.as_view(),
         name='basic_product__detail'),
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
    # user
    path('user/list', views.user.UserList.as_view(), name='user__list'),

]
