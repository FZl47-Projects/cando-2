from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django import forms

from apps.core.models import Image
from apps.core import get_settings
from apps.core.utils import now_shamsi_date, convert_str_to_shamsi_date
from . import models


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

        if not self.cleaned_data.get('image_cover'):
            # set default image
            self.set_default_image_cover()

    def set_default_categories(self):
        default_categories = models.Category.objects.filter(default=True)
        if not default_categories:
            # create default category
            default_categories = [models.Category.objects.create(
                name=get_settings().OBJECTS['CATEGORY']['default_name'],
                default=True  # default category
            )]
        self.cleaned_data['categories'] = default_categories

    def set_default_image_cover(self):
        with open(get_settings().IMAGE['DEFAULT_IMAGE_PATH'], 'rb') as file:
            default_image_data = file.read()
        default_image_file = ContentFile(default_image_data, name='default.png')
        image_cover_obj = Image.objects.create(image=default_image_file)
        self.cleaned_data['image_cover'] = image_cover_obj


class BasicProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.BasicProduct
        fields = '__all__'


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
        if not self.is_valid():
            return
        # create image's obj
        images = files.getlist('images', None)
        images_obj = []
        if images:
            for image in images:
                images_obj.append(Image(image=image))
            images_obj = Image.objects.bulk_create(images_obj)
            self.cleaned_data['images'] = images_obj


class ProductCartCreateForm(forms.ModelForm):
    # TODO: should test and complete
    class Meta:
        model = models.ProductCart
        fields = '__all__'


class ProductOptionsCartCreateForm(forms.ModelForm):
    # TODO: should test and complete
    class Meta:
        model = models.ProductCartOption
        fields = '__all__'
