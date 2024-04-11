from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import TemplateView, ListView, View

from apps.core.utils import now_shamsi_date
from apps.core.mixins.views import (
    CreateViewMixin, UpdateViewMixin, UpdateMultipleObjViewMixin,
    FilterSimpleListViewMixin, DeleteMixin
)
from apps.product import models, forms


class BasicProductCreate(CreateViewMixin, TemplateView):
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


class BasicProductList(FilterSimpleListViewMixin, ListView):
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


class BasicProductDetail(TemplateView):
    template_name = 'dashboard/admin/product/product/basic/detail.html'

    def get_context_data(self, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(models.BasicProduct, id=product_id)
        context = {
            'product': product
        }
        return context


class CustomProductList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('user__phonenumber__icontains',)
    filter_fields = ('type', 'status__status')
    template_name = 'dashboard/admin/product/custom-product/list.html'

    def get_queryset(self):
        objects = models.CustomProduct.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class CustomProductDetail(TemplateView):
    template_name = 'dashboard/admin/product/custom-product/detail.html'

    def get_context_data(self, **kwargs):
        custom_product_id = kwargs.get('custom_product_id')
        custom_product = get_object_or_404(models.CustomProduct, id=custom_product_id)
        context = {
            'custom_product': custom_product
        }
        return context


class CustomProductDelete(DeleteMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:custom_product__list')

    def get_object(self, request, *args, **kwargs):
        custom_product_id = kwargs.get('custom_product_id')
        return get_object_or_404(models.CustomProduct, id=custom_product_id)


class CustomProductManageStatus(UpdateViewMixin, View):
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


class CategoryList(FilterSimpleListViewMixin, ListView):
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


class CategoryCreate(CreateViewMixin, View):
    form = forms.CategoryCreateForm
    success_message = _('Category Created Successfully')
    redirect_url = reverse_lazy('dashboard:category__list')


class TagList(FilterSimpleListViewMixin, ListView):
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


class TagCreate(CreateViewMixin, View):
    form = forms.TagCreateForm
    success_message = _('Tag Created Successfully')
    redirect_url = reverse_lazy('dashboard:tag__list')


class ProductAttrCategoryList(FilterSimpleListViewMixin, ListView):
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


class ProductAttrCategoryCreate(CreateViewMixin, View):
    form = forms.ProductAttrCategoryCreateForm
    success_message = _('Product Attribute Category Created Successfully')
    redirect_url = reverse_lazy('dashboard:product_attr_category__list')


class ProductAttrGroupList(FilterSimpleListViewMixin, ListView):
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


class ProductAttrGroupCreate(CreateViewMixin, View):
    form = forms.ProductAttrGroupCreateForm
    success_message = _('Product Attribute Group Created Successfully')
    redirect_url = reverse_lazy('dashboard:product_attr_group__list')


class ProductAttrFieldList(FilterSimpleListViewMixin, ListView):
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


class ProductAttrFieldCreate(CreateViewMixin, View):
    form = forms.SimpleProductAttrCreateForm
    success_message = _('Product Attribute Field Created Successfully')
    redirect_url = reverse_lazy('dashboard:product_attr_field__list')


class CommentList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('text__icontains', 'user__phonenumber__icontains', 'product__title__icontains')
    filter_fields = ('status', 'rate')
    template_name = 'dashboard/admin/product/comment/list.html'

    def get_queryset(self):
        objects = models.Comment.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class CommentDetail(TemplateView):
    template_name = 'dashboard/admin/product/comment/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_id = kwargs['comment_id']
        comment = get_object_or_404(models.Comment, id=comment_id)
        context['comment'] = comment
        return context


class CommentDelete(DeleteMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:comment__list')

    def get_object(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        return get_object_or_404(models.Comment, id=comment_id)


class CommentManageStatus(UpdateMultipleObjViewMixin, View):
    """
        group actions
        approve or reject product comment
    """
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


class DiscountCouponList(FilterSimpleListViewMixin, ListView):
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


class DiscountCouponCreate(CreateViewMixin, View):
    """
        group actions
        approve or reject product comment
    """
    form = forms.DiscountCouponCreateForm
    success_message = _('Discount Coupon Created Successfully')
    redirect_url = reverse_lazy('dashboard:discount_coupon__list')


class FactorCakeImageList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('user_name__icontains', 'factor_code__icontains')
    filter_fields = ('status',)
    template_name = 'dashboard/admin/product/factor-cake-image/list.html'

    def get_queryset(self):
        objects = models.FactorCakeImage.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class FactorCakeImageDetail(TemplateView):
    template_name = 'dashboard/admin/product/factor-cake-image/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        factor_cake_image_id = kwargs['factor_cake_image_id']
        factor_cake_image = get_object_or_404(models.FactorCakeImage, id=factor_cake_image_id)
        # seen
        factor_cake_image.status = 'seen'
        factor_cake_image.save()
        context['factor_cake_image'] = factor_cake_image
        return context


class FactorCakeImageDelete(DeleteMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:factor_cake_image__list')

    def get_object(self, request, *args, **kwargs):
        factor_cake_image_id = kwargs.get('factor_cake_image_id')
        return get_object_or_404(models.FactorCakeImage, id=factor_cake_image_id)
