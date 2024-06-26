from django.shortcuts import get_object_or_404, Http404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import TemplateView, ListView, View

from apps.core.utils import now_shamsi_date
from apps.core.auth import object_access
from apps.core.mixins.views import (
    CreateViewMixin, UpdateViewMixin, UpdateMultipleObjViewMixin,
    CreateOrUpdateViewMixin, MultipleUserViewMixin, MultipleUserListViewMixin,
    FilterSimpleListViewMixin, DeleteViewMixin,
    UserRoleViewMixin
)
from apps.product import models, forms


class BasicProductCreate(UserRoleViewMixin, CreateViewMixin, TemplateView):
    role_access = ('super_user',)
    form = forms.BasicProductCreateForm
    success_message = _('Product Created Successfully')
    redirect_url = reverse_lazy('dashboard:basic_product__create')
    template_name = 'dashboard/admin/product/product/basic/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': models.Category.objects.exclude(default=True),
            'tags': models.Tag.objects.all(),
            'attr_categories': models.ProductAttrCategory.objects.all()
        })
        return context


class BasicProductList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('title__icontains',)
    filter_fields = ('type', 'status', 'categories')
    template_name = 'dashboard/admin/product/product/basic/list.html'

    def get_queryset(self):
        objects = models.BasicProduct.objects.get_list()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        context['categories'] = models.Category.objects.order_by('-default')
        return context

    def filter(self, objects):
        objects = super().filter(objects)
        # advance filter
        request = self.request
        p_stock = request.GET.get('stock_status')
        # by stock
        if p_stock and p_stock != 'all':
            if p_stock == 'in_stock':
                objects = objects.filter(productinventory__quantity__gt=0)
            else:
                objects = objects.filter(productinventory__quantity__lte=0)
        return objects


class BasicProductDetail(UserRoleViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/product/basic/detail.html'

    def get_context_data(self, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(models.BasicProduct, id=product_id)
        context = {
            'product': product,
            # additional objects
            'categories': models.Category.objects.all(),
            'tags': models.Tag.objects.all(),
            'attr_categories': models.ProductAttrCategory.objects.all()
        }
        return context


class BasicProductUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    form = forms.BasicProductUpdateForm
    success_message = _('Operation Successfully Completed')

    def get_object(self):
        product_id = self.kwargs['product_id']
        return get_object_or_404(models.BasicProduct, id=product_id)


class BasicProductImagesUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    form = forms.BasicProductImagesUpdateForm
    success_message = _('Operation Successfully Completed')

    def get_object(self):
        product_id = self.kwargs['product_id']
        return get_object_or_404(models.BasicProduct, id=product_id)


class BasicProductDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:basic_product__list')

    def get_object(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        return get_object_or_404(models.BasicProduct, id=product_id)


class CustomProductList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('user__phonenumber__icontains',)
    filter_fields = ('type', 'status__status')
    super_user_template = 'dashboard/admin/product/custom-product/list.html'
    user_template = 'dashboard/user/product/custom-product/list.html'

    def get_super_user_queryset(self):
        objects = models.CustomProduct.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_user_queryset(self):
        objects = self.request.user.get_custom_products()
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class CustomProductDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/product/custom-product/detail.html'
    user_template = 'dashboard/user/product/custom-product/detail.html'

    def get_context_data(self, **kwargs):
        custom_product_id = kwargs.get('custom_product_id')
        custom_product = models.CustomProduct.objects.get_subclass(id=custom_product_id)
        if not custom_product:
            raise Http404
        object_access(custom_product, self.request.user)
        context = {
            'custom_product': custom_product
        }
        return context


class CustomProductDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:custom_product__list')

    def get_object(self, request, *args, **kwargs):
        custom_product_id = kwargs.get('custom_product_id')
        custom_product = models.CustomProduct.objects.get_subclass(id=custom_product_id)
        if not custom_product:
            raise Http404
        return custom_product


class CustomProductManageStatus(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')

    def get_object(self):
        custom_product_id = self.kwargs['custom_product_id']
        return get_object_or_404(models.CustomProduct, id=custom_product_id).status

    def get_form(self):
        data = self.get_data()
        status = data.get('status')
        if status == 'accepted':
            return forms.CustomProductAcceptStatusForm
        else:
            return forms.CustomProductRejectStatusForm

    def get_redirect_url(self):
        if self.is_success:
            return self.obj.custom_product.get_dashboard_absolute_url()
        return super().get_redirect_url()


class CustomProductCakeAttrCategoryManage(UserRoleViewMixin, CreateOrUpdateViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/custom-product/settings/cake-attr-category.html'
    form = forms.CustomProductCakeAttrCategoryManageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['custom_product_attr_category'] = self.get_object()
        context['groups'] = models.ProductAttrGroup.objects.all()
        return context

    def get_object(self):
        custom_product_attr_category = models.CustomProductCakeAttrCategory.objects.first()
        return custom_product_attr_category  # return object or None

    def set_success_message(self):
        if self.is_create_state():
            self.success_message = _('Custom Product Attr Category Created Successfully')
        else:
            self.success_message = _('Custom Product Attr Category Updated Successfully')
        super().set_success_message()


class CustomProductSweetsAttrCategoryManage(UserRoleViewMixin, CreateOrUpdateViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/custom-product/settings/sweets-attr-category.html'
    form = forms.CustomProductSweetsAttrCategoryManageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['custom_product_attr_category'] = self.get_object()
        context['groups'] = models.ProductAttrGroup.objects.all()
        return context

    def get_object(self):
        custom_product_attr_category = models.CustomProductSweetsAttrCategory.objects.first()
        return custom_product_attr_category  # return object or None

    def set_success_message(self):
        if self.is_create_state():
            self.success_message = _('Custom Product Attr Category Created Successfully')
        else:
            self.success_message = _('Custom Product Attr Category Updated Successfully')
        super().set_success_message()


class ProductInventoryUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    form = forms.ProductInventoryUpdateForm

    def get_object(self):
        inventory_id = self.kwargs['inventory_id']
        return get_object_or_404(models.ProductInventory, id=inventory_id)


class ProductInventoryDefaultManage(UserRoleViewMixin, CreateOrUpdateViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/inventory/settings/manage.html'
    form = forms.ProductInventoryDefaultManageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['default_inventory'] = self.get_object()
        return context

    def get_object(self):
        return models.ProductInventoryDefault.objects.first()  # return object or None

    def set_success_message(self):
        if self.is_create_state():
            self.success_message = _('Default Inventory Created Successfully')
        else:
            self.success_message = _('Default Inventory Updated Successfully')
        super().set_success_message()


class CategoryList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('name__icontains',)
    template_name = 'dashboard/admin/product/category/list.html'

    def get_queryset(self):
        objects = models.Category.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class CategoryCreate(UserRoleViewMixin, CreateViewMixin, View):
    role_access = ('super_user',)
    form = forms.CategoryCreateForm
    success_message = _('Category Created Successfully')
    redirect_url = reverse_lazy('dashboard:category__list')


class CategoryDetail(UserRoleViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/category/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = kwargs['category_id']
        category = get_object_or_404(models.Category, id=category_id)
        context['category'] = category
        return context


class CategoryUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    form = forms.CategoryUpdateForm

    def get_object(self):
        category_id = self.kwargs['category_id']
        return get_object_or_404(models.Category, id=category_id)


class CategoryDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:category__list')

    def get_object(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        return get_object_or_404(models.Category, id=category_id)


class TagList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('name__icontains',)
    template_name = 'dashboard/admin/product/tag/list.html'

    def get_queryset(self):
        objects = models.Tag.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class TagDetail(UserRoleViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/tag/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = kwargs['tag_id']
        tag = get_object_or_404(models.Tag, id=tag_id)
        context['tag'] = tag
        return context


class TagDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:tag__list')

    def get_object(self, request, *args, **kwargs):
        tag_id = kwargs.get('tag_id')
        return get_object_or_404(models.Tag, id=tag_id)


class TagCreate(UserRoleViewMixin, CreateViewMixin, View):
    role_access = ('super_user',)
    form = forms.TagCreateForm
    success_message = _('Tag Created Successfully')
    redirect_url = reverse_lazy('dashboard:tag__list')


class ProductAttrCategoryCreate(UserRoleViewMixin, CreateViewMixin, View):
    role_access = ('super_user',)
    form = forms.ProductAttrCategoryCreateForm
    success_message = _('Product Attribute Category Created Successfully')
    redirect_url = reverse_lazy('dashboard:product_attr_category__list')


class ProductAttrCategoryList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('name__icontains',)
    template_name = 'dashboard/admin/product/attributes/category/list.html'

    def get_queryset(self):
        objects = models.ProductAttrCategory.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        context['groups'] = models.ProductAttrGroup.objects.all()
        return context


class ProductAttrCategoryDetail(UserRoleViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/attributes/category/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = kwargs['category_id']
        category = get_object_or_404(models.ProductAttrCategory, id=category_id)
        context['category'] = category
        context['groups'] = models.ProductAttrGroup.objects.all()
        return context


class ProductAttrCategoryUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    form = forms.ProductAttrCategoryUpdateForm

    def get_object(self):
        category_id = self.kwargs.get('category_id')
        return get_object_or_404(models.ProductAttrCategory, id=category_id)


class ProductAttrCategoryDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:product_attr_category__list')

    def get_object(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        return get_object_or_404(models.ProductAttrCategory, id=category_id)


class ProductAttrGroupCreate(UserRoleViewMixin, CreateViewMixin, View):
    role_access = ('super_user',)
    form = forms.ProductAttrGroupCreateForm
    success_message = _('Product Attribute Group Created Successfully')
    redirect_url = reverse_lazy('dashboard:product_attr_group__list')


class ProductAttrGroupList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('name__icontains',)
    template_name = 'dashboard/admin/product/attributes/group/list.html'

    def get_queryset(self):
        objects = models.ProductAttrGroup.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        context['fields'] = models.SimpleProductAttr.objects.all()
        return context


class ProductAttrGroupDetail(UserRoleViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/attributes/group/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = kwargs['group_id']
        group = get_object_or_404(models.ProductAttrGroup, id=group_id)
        context['group'] = group
        context['fields'] = models.SimpleProductAttr.objects.all()
        return context


class ProductAttrGroupUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    form = forms.ProductAttrGroupUpdateForm

    def get_object(self):
        group_id = self.kwargs['group_id']
        return get_object_or_404(models.ProductAttrGroup, id=group_id)


class ProductAttrGroupDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:product_attr_group__list')

    def get_object(self, request, *args, **kwargs):
        group_id = kwargs.get('group_id')
        return get_object_or_404(models.ProductAttrGroup, id=group_id)


class ProductAttrFieldCreate(UserRoleViewMixin, CreateViewMixin, View):
    role_access = ('super_user',)
    form = forms.SimpleProductAttrCreateForm
    success_message = _('Product Attribute Field Created Successfully')
    redirect_url = reverse_lazy('dashboard:product_attr_field__list')


class ProductAttrFieldList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('name__icontains',)
    template_name = 'dashboard/admin/product/attributes/field/list.html'

    def get_queryset(self):
        objects = models.SimpleProductAttr.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class ProductAttrFieldDetail(UserRoleViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/product/attributes/field/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_id = kwargs['field_id']
        field = get_object_or_404(models.SimpleProductAttr, id=field_id)
        context['field'] = field
        return context


class ProductAttrFieldUpdate(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    form = forms.SimpleProductAttrUpdateForm

    def get_object(self):
        field_id = self.kwargs.get('field_id')
        return get_object_or_404(models.SimpleProductAttr, id=field_id)


class ProductAttrFieldDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:product_attr_field__list')

    def get_object(self, request, *args, **kwargs):
        field_id = kwargs.get('field_id')
        return get_object_or_404(models.SimpleProductAttr, id=field_id)


class CommentList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('text__icontains', 'user__phonenumber__icontains', 'product__title__icontains')
    filter_fields = ('status', 'rate')
    super_user_template = 'dashboard/admin/product/comment/list.html'
    user_template = 'dashboard/user/product/comment/list.html'

    def get_super_user_queryset(self):
        objects = models.Comment.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_user_queryset(self):
        objects = self.request.user.get_all_comments()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class CommentDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/product/comment/detail.html'
    user_template = 'dashboard/user/product/comment/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_id = kwargs['comment_id']
        comment = get_object_or_404(models.Comment, id=comment_id)
        object_access(comment, self.request.user)
        context['comment'] = comment
        return context


class CommentDelete(DeleteViewMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:comment__list')

    def get_object(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = get_object_or_404(models.Comment, id=comment_id)
        object_access(comment, self.request.user)
        return comment


class CommentManageStatus(UserRoleViewMixin, UpdateMultipleObjViewMixin, View):
    """
        group actions
        approve or reject product comment
    """
    role_access = ('super_user',)
    form = forms.CommentManageStatusForm

    def get_objects(self):
        data = self.request.POST
        comment_ids = data.getlist('comments', [])
        comments = models.Comment.objects.filter(id__in=comment_ids)
        return comments

    def set_success_message(self):
        objects = self.get_updated_objects()
        if len(objects) == 1:
            comment = objects[0]
            if comment.status == 'rejected':
                messages.success(self.request, _('Product Comment Has Been Successfully Rejected'))
            elif comment.status == 'accepted':
                messages.success(self.request, _('Product Comment Has Been Successfully Approved'))
            return
        messages.success(self.request, _('Product Comment Has Been Processed'))


class DiscountCouponList(UserRoleViewMixin, FilterSimpleListViewMixin, ListView):
    role_access = ('super_user',)
    paginate_by = 20
    search_fields = ('code__icontains', 'price', 'count')
    template_name = 'dashboard/admin/product/discount/coupon/list.html'

    def get_queryset(self):
        objects = models.DiscountCoupon.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context

    def filter(self, objects):
        objects = super().filter(objects)
        # advance filter
        # filter by available
        p_available = self.request.GET.get('available')
        if p_available and p_available != 'all':
            if p_available == 'true':
                objects = objects.filter(expire_at__gt=str(now_shamsi_date()), count__gt=0)
            else:
                objects = objects.filter(Q(expire_at__lte=str(now_shamsi_date())) | Q(count__lte=0))
        return objects


class DiscountCouponCreate(UserRoleViewMixin, CreateViewMixin, View):
    """
        group actions
        approve or reject product comment
    """
    role_access = ('super_user',)
    form = forms.DiscountCouponCreateForm
    success_message = _('Discount Coupon Created Successfully')
    redirect_url = reverse_lazy('dashboard:discount_coupon__list')


class FactorCakeImageList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('user_name__icontains', 'factor_code__icontains')
    filter_fields = ('status',)
    super_user_template = 'dashboard/admin/product/factor-cake-image/list.html'
    user_template = 'dashboard/user/product/factor-cake-image/list.html'

    def get_super_user_queryset(self):
        objects = models.FactorCakeImage.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_user_queryset(self):
        objects = self.request.user.get_factor_cake_images()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class FactorCakeImageDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/product/factor-cake-image/detail.html'
    user_template = 'dashboard/user/product/factor-cake-image/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        factor_cake_image_id = kwargs['factor_cake_image_id']
        factor_cake_image = get_object_or_404(models.FactorCakeImage, id=factor_cake_image_id)
        object_access(factor_cake_image, self.request.user)
        if factor_cake_image.status != 'seen' and self.request.user != factor_cake_image.user:
            # seen
            factor_cake_image.status = 'seen'
            factor_cake_image.save()
        context['factor_cake_image'] = factor_cake_image
        return context


class FactorCakeImageDelete(DeleteViewMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:factor_cake_image__list')

    def get_object(self, request, *args, **kwargs):
        factor_cake_image_id = kwargs.get('factor_cake_image_id')
        factor_cake_image = get_object_or_404(models.FactorCakeImage, id=factor_cake_image_id)
        object_access(factor_cake_image, self.request.user)
        return factor_cake_image


class OrderList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('user__phonenumber__icontains', 'tc__icontains', 'invoice__purchase__price_paid__icontains',)
    filter_fields = ('status__status',)
    super_user_template = 'dashboard/admin/product/order/list.html'
    user_template = 'dashboard/user/product/order/list.html'

    def get_super_user_queryset(self):
        objects = models.Cart.objects.exclude(invoice__purchase=None)
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_user_queryset(self):
        objects = self.request.user.get_orders()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context

    def search(self, objects):
        objects = super().search(objects)
        # advance search(product,)
        spr = self.request.GET.get('spr')
        if not spr:
            return objects
        objects = objects.filter(productcart__product__id=spr)
        return objects


class OrderDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/product/order/detail.html'
    user_template = 'dashboard/user/product/order/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order_id = kwargs['order_id']
        order = get_object_or_404(models.Cart, id=order_id)
        object_access(order, self.request.user)
        context['order'] = order
        return context


class OrderDelete(UserRoleViewMixin, DeleteViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:order__list')

    def get_object(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        return get_object_or_404(models.Cart, id=order_id)


class OrderManageStatus(UserRoleViewMixin, UpdateViewMixin, View):
    role_access = ('super_user',)
    success_message = _('Operation Successfully Completed')
    form = forms.CartStatusManageStatusForm

    def get_object(self):
        order_status_id = self.kwargs['order_status_id']
        return get_object_or_404(models.CartStatus, id=order_status_id)

    def add_additional_data(self, data, obj=None):
        data['cart'] = obj.cart
