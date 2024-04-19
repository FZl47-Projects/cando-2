from django.views.generic import ListView

from apps.core.mixins.views import FilterSimpleListViewMixin
from apps.account import models


class UserList(FilterSimpleListViewMixin, ListView):
    paginate_by = 20
    search_fields = ('phonenumber__icontains',)
    filter_fields = ('is_active',)
    template_name = 'dashboard/admin/user/list.html'

    def get_queryset(self):
        objects = models.User.objects.all()
        objects = self.search(objects)
        objects = self.filter(objects)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context
