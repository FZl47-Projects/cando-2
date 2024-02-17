from django.views.generic import View, TemplateView, DetailView
from apps.core.auth.mixins import LoginRequiredMixinCustom


# Render AdminDashboard view
class AdminDashboardView(LoginRequiredMixinCustom, TemplateView):
    template_name = 'dashboard/admin/index.html'
