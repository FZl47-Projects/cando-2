from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView, View
from django.contrib import messages

from apps.core.auth.mixins import LoginRequiredMixinCustom
from apps.core.utils import form_validate_err
from .models import Address
from . import forms


# Create Address view
class CreateAddressView(LoginRequiredMixinCustom, View):
    def get_url(self, request):
        redirect_url = request.POST.get('redirect_path')
        return redirect_url or reverse('account:profile') + '?tab=address'

    def post(self, request):
        data = request.POST.copy()
        data.update({
            'user': request.user,
        })

        form = forms.CreateAddressForm(data=data)
        if form_validate_err(request, form):
            form.save()

            messages.success(request, _('Address successfully added'))

        return redirect(self.get_url(request))  # Redirect to previous url


# Delete Address view
class DeleteAddressView(LoginRequiredMixinCustom, View):
    def get_url(self, request):
        redirect_url = request.POST.get('redirect_path')
        return redirect_url or reverse('account:profile') + '?tab=address'

    def post(self, request):
        pk = request.POST.get('pk')
        try:
            obj = Address.objects.get(pk=pk)
            obj.delete()
            messages.success(request, _('Address successfully deleted'))
        except Address.DoesNotExist:
            messages.error(request, _('There is an issue. please try again'))

        return redirect(self.get_url(request))
