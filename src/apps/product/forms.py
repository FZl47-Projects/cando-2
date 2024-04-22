from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django import forms

from apps.storage.models import Image
from apps.core import get_settings
from apps.core.utils import (now_shamsi_date,
                             convert_str_to_shamsi_date,
                             log_event,
                             create_form_messages)
from . import models

settings = get_settings()


class AttributesFieldUtil:

    @classmethod
    def create_attrs_by_groups(cls, data, groups):
        attrs_selected = []
        for group in groups:
            """
                product_group_{id} seted in template(product-)
            """
            attr_id = data.get('product_group_{}'.format(group.id))
            if not attr_id:
                continue
            attr_selected_data = {
                'group': group.id,
                'attr': attr_id
            }
            f = ProductAttrSelectCreateForm(attr_selected_data)
            if not f.is_valid():
                print(f.errors)
                log_event(_('Product Field DoesNotExist | There Is Some Problem In Selected Attributes'), 'ERROR')
                raise ValueError(_('There Is Some Problem In Selected Attributes'))
            attr_selected_obj = f.save()
            attrs_selected.append(attr_selected_obj)
        return attrs_selected


class BasicProductCreateForm(forms.ModelForm):
    class Meta:
        model = models.BasicProduct
        fields = '__all__'

    def clean(self):
        super().clean()
        files = self.files
        if not self.is_valid():
            return
        # create image's objects
        image_cover_file = files.get('image_cover_file')
        images_file = files.getlist('images_file')
        # create image cover obj
        if image_cover_file:
            image_cover_obj = Image.objects.create(image=image_cover_file)
            self.cleaned_data['image_cover'] = image_cover_obj
        # create image objs
        if images_file:
            images_file_objs = []
            for img_file in images_file:
                images_file_objs.append(
                    Image(image=img_file)
                )
            images_file_objs = Image.objects.bulk_create(images_file_objs)
            self.cleaned_data['images'] = images_file_objs

        if not self.cleaned_data.get('categories'):
            # set default category
            self.set_default_categories()

        if not self.cleaned_data.get('image_cover') and not self.instance:
            # set default image
            self.set_default_image_cover()

    def set_default_categories(self):
        default_categories = models.Category.objects.filter(default=True)
        if not default_categories:
            # create default category
            default_categories = [models.Category.objects.create(
                name=settings.OBJECTS['CATEGORY']['default_name'],
                default=True  # default category
            )]
        self.cleaned_data['categories'] = default_categories

    def set_default_image_cover(self):
        with open(settings.IMAGE['DEFAULT_IMAGE_PATH'], 'rb') as file:
            default_image_data = file.read()
        default_image_file = ContentFile(default_image_data, name='default.png')
        image_cover_obj = Image.objects.create(image=default_image_file)
        self.cleaned_data['image_cover'] = image_cover_obj


class BasicProductUpdateForm(BasicProductCreateForm):
    class Meta:
        model = models.BasicProduct
        exclude = ('image_cover', 'images')


class BasicProductImagesUpdateForm(BasicProductCreateForm):
    class Meta:
        model = models.BasicProduct
        fields = ('image_cover', 'images')


class ProductAttrCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = models.ProductAttrCategory
        fields = '__all__'


class ProductAttrGroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.ProductAttrGroup
        fields = '__all__'


class SimpleProductAttrCreateForm(forms.ModelForm):
    class Meta:
        model = models.SimpleProductAttr
        fields = '__all__'


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = '__all__'


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('product', 'user', 'text', 'rate')


class CommentManageStatusForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('status',)


class DiscountCouponCreateForm(forms.ModelForm):
    class Meta:
        model = models.DiscountCoupon
        fields = '__all__'

    def clean(self):
        super().clean()

        # validation expire_at field
        field_expire_at = self.data.get('expire_at')
        if field_expire_at:
            if convert_str_to_shamsi_date(field_expire_at) < now_shamsi_date():
                self.add_error('expire_at', _('You Should Set A Time In The Future, Not In The Past'))


class FactorCakeImageCreateForm(forms.ModelForm):
    description = forms.CharField(max_length=300, required=False)

    class Meta:
        model = models.FactorCakeImage
        exclude = ('status',)

    def clean(self):
        super().clean()
        files = self.files
        request = self.data['request']
        user = request.user
        if not self.is_valid():
            return
        # add user if exist
        self.cleaned_data['user'] = user if user.is_authenticated == True else None

        # create image's obj
        images = files.getlist('images', None)
        images_obj = []
        if images:
            for image in images:
                images_obj.append(Image(image=image))
            images_obj = Image.objects.bulk_create(images_obj)
            self.cleaned_data['images'] = images_obj


class ProductCartCreateForm(forms.ModelForm):
    # prevent check 'attr_selected' field
    product = forms.CharField(max_length=10, required=False)
    cart = forms.CharField(max_length=10, required=False)
    attrs_selected = forms.CharField(max_length=10, required=False)

    class Meta:
        model = models.ProductCart
        fields = '__all__'

    def get_request(self):
        return self.data['request']

    def get_product(self):
        product_id = self.data['product_id']
        product = get_object_or_404(models.BasicProduct, id=product_id)
        return product

    def check_stock_product_in_cart(self, product, cart):
        product_cart = cart.productcart_set.filter(product=product, cart=cart)
        if product_cart.exists():
            product_cart_quantities = product_cart.aggregate(total_quantity=models.models.Sum('quantity'))[
                                          'total_quantity'] or 0
            quantity = int(self.data['quantity'])
            if (product_cart_quantities + quantity) > product.get_quantity():
                return False
        return True

    def clean(self):
        product = self.get_product()
        request = self.get_request()
        user = request.user
        if user.is_authenticated:
            cart = user.get_current_cart_or_create()
        else:
            cart = models.Cart.get_session_cart(request)
        # check product stock and (stock cart)
        if (not product.has_in_stock()) or (not self.check_stock_product_in_cart(product, cart)):
            self.add_error('quantity', _('There Are Too Many Products In Your Shopping Cart'))
            return
        try:
            attrs_selected = AttributesFieldUtil.create_attrs_by_groups(self.data, product.get_attr_groups())
            # add attrs to clean data
            self.cleaned_data['attrs_selected'] = attrs_selected
        except ValueError as e:
            self.add_error('attrs_selected', e.__str__())

        # add additional data
        self.cleaned_data['product'] = product
        self.cleaned_data['cart'] = cart
        super().clean()


class ProductAttrSelectCreateForm(forms.ModelForm):
    class Meta:
        model = models.ProductAttrSelected
        fields = '__all__'


class CustomProductCreateForm(forms.ModelForm):
    description = forms.CharField(max_length=300, required=False)
    writing_on = forms.CharField(max_length=100, required=False)
    images = forms.ImageField(required=False)
    # prevent check 'attr_selected' field
    attrs_selected = forms.CharField(max_length=10, required=False)

    class Meta:
        model = models.CustomProduct
        fields = '__all__'

    def clean(self):
        super().clean()

        files = self.files
        if not self.is_valid():
            return

        data = self.data
        # create attributes selected
        custom_pr_category = models.CustomProductAttrCategory.objects.first()
        if custom_pr_category:
            try:
                attrs_selected = AttributesFieldUtil.create_attrs_by_groups(data, custom_pr_category.get_groups())
                self.cleaned_data['attrs_selected'] = attrs_selected
            except ValueError as e:
                self.add_error('attrs_selected', e.__str__())
        else:
            log_event(_('You Should Create Custom Product Category Fields'), 'ERROR')

        # create image's obj
        images = files.getlist('images', None)
        images_obj = []
        if images:
            for image in images:
                images_obj.append(Image(image=image))
            images_obj = Image.objects.bulk_create(images_obj)
            self.cleaned_data['images'] = images_obj


class CustomProductRejectStatusForm(forms.ModelForm):
    class Meta:
        model = models.CustomProductStatus
        fields = ('note', 'custom_product', 'status')


class CustomProductAcceptStatusForm(forms.ModelForm):
    class Meta:
        model = models.CustomProductStatus
        fields = ('note', 'custom_product', 'status', 'price')


class CustomProductAttrCategoryManageForm(forms.ModelForm):
    class Meta:
        model = models.CustomProductAttrCategory
        fields = '__all__'


class CartStatusManageStatusForm(forms.ModelForm):
    class Meta:
        model = models.CartStatus
        fields = '__all__'


class ProductInventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ProductInventory
        fields = '__all__'


class ProductInventoryDefaultManageForm(forms.ModelForm):
    class Meta:
        model = models.ProductInventoryDefault
        fields = '__all__'
