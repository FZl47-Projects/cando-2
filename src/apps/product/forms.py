from django import forms
from . import models


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'


# class FactorCakeImageForm(forms.ModelForm):
#     description = forms.CharField(max_length=400, required=False)
#
#     class Meta:
#         model = models.FactorCakeImage
#         exclude = ('images',)
#
#
# class FactorCreateForm(forms.ModelForm):
#     note = forms.CharField(required=False)
#
#     class Meta:
#         model = models.Factor
#         exclude = ('track_code',)


# class FactorCreateNonAddressForm(forms.ModelForm):
#     note = forms.CharField(required=False)
#
#     class Meta:
#         model = models.Factor
#         exclude = ('track_code', 'address')


# class CartStatusForm(forms.ModelForm):
#     class Meta:
#         model = models.CartStatus
#         fields = '__all__'


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('product', 'user', 'title', 'description', 'rate')


# class CustomOrderProductAccept(forms.ModelForm):
#     note = forms.CharField(max_length=1000, required=False)
#
#     class Meta:
#         model = models.CustomOrderProduct
#         fields = ('note', 'price', 'is_checked', 'cart', 'status')
#
#
# class CustomOrderProductReject(forms.ModelForm):
#     note = forms.CharField(max_length=1000, required=False)
#
#     class Meta:
#         model = models.CustomOrderProduct
#         fields = ('note', 'status')
