from django.views.generic import View, TemplateView, DetailView
from apps.core.auth.mixins import AdminRequiredMixin


# Render AdminDashboard view
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/index.html'
