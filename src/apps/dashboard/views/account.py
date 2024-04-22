from django.views.generic import ListView, TemplateView, View
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from apps.core.mixins.views import FilterSimpleListViewMixin, DeleteViewMixin, UpdateViewMixin
from apps.account import models, forms


class UserList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('phonenumber__icontains',)
    filter_fields = ('is_active', 'role')
    template_name = 'dashboard/admin/account/user/list.html'

    def get_queryset(self):
        objects = models.User.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


class UserDetail(TemplateView):
    template_name = 'dashboard/admin/account/user/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        # user = get_object_or_404(models.User, id=user_id, role__in=['normal_user', 'operator_user'])
        user = get_object_or_404(models.User, id=user_id)
        context['user'] = user
        return context


class UserUpdate(UpdateViewMixin, View):
    form = forms.UserUpdateByAdminForm
    success_message = _('User Updated Successfully')

    def get_object(self):
        user_id = self.kwargs['user_id']
        return get_object_or_404(models.User, id=user_id)


class UserDelete(DeleteViewMixin, View):
    success_message = _('Operation Successfully Completed')
    redirect_url = reverse_lazy('dashboard:user__list')

    def get_object(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        return get_object_or_404(models.User, id=user_id)
