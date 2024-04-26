from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, View
from django.shortcuts import get_object_or_404

from apps.core.auth import object_access
from apps.core.settings import get_default_address
from apps.core.mixins.views import (UserRoleViewMixin, CreateOrUpdateViewMixin,
                                    MultipleUserViewMixin, UpdateViewMixin,
                                    MultipleUserListViewMixin, FilterSimpleListViewMixin,
                                    CreateViewMixin
                                    )
from apps.navigation import forms, models


class DefaultAddressManage(UserRoleViewMixin, CreateOrUpdateViewMixin, TemplateView):
    role_access = ('super_user',)
    template_name = 'dashboard/admin/navigation/address/settings/address-default.html'
    form = forms.DefaultAddressManageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['address'] = self.get_object()
        return context

    def get_object(self):
        default_address = get_default_address().first()
        return default_address  # return object or None

    def set_success_message(self):
        if self.is_create_state():
            self.success_message = _('Default Address Created Successfully')
        else:
            self.success_message = _('Default Address Updated Successfully')
        super().set_success_message()


class AddressCreate(CreateViewMixin, View):
    form = forms.AddressCreateForm
    success_message = _('Address Created Successfully')


class AddressList(MultipleUserListViewMixin, FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('title__icontains',)
    user_template = 'dashboard/user/navigation/address/list.html'

    def get_user_queryset(self):
        objects = self.request.user.get_addresses()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class AddressDetail(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/navigation/address/detail.html'
    user_template = 'dashboard/user/navigation/address/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        address_id = kwargs['address_id']
        address = get_object_or_404(models.Address, id=address_id)
        object_access(address, self.request.user)
        context['address'] = address
        return context


class AddressUpdate(UpdateViewMixin, TemplateView):
    success_message = _('Operation Successfully Completed')
    form = forms.AddressUpdateForm

    def get_object(self):
        address_id = self.kwargs['address_id']
        address = get_object_or_404(models.Address, id=address_id)
        object_access(address, self.request.user)
        return address
