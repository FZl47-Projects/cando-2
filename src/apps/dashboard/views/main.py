from django.views.generic import TemplateView
from apps.core.auth.mixins import LoginRequiredMixinCustom


class Index(LoginRequiredMixinCustom, TemplateView):
    template_name = 'dashboard/admin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
