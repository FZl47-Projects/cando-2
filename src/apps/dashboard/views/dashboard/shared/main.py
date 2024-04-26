from django.views.generic import TemplateView

from apps.core.mixins.views import MultipleUserViewMixin


class Index(MultipleUserViewMixin, TemplateView):
    super_user_template = 'dashboard/admin/index.html'
    user_template = 'dashboard/user/index.html'

