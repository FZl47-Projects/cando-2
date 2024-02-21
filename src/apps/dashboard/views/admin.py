from django.views.generic import View, TemplateView, DetailView
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib import messages

from apps.core.auth.mixins import AdminRequiredMixin
from apps.core.utils import form_validate_err
from apps.account import forms


# Render AdminDashboard view
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/index.html'


# Render AdminProfile view
class AdminProfileView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/profile_details.html'

    def post(self, request):
        form = forms.UpdateProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if form_validate_err(request, form):
            form.save(commit=False)
            messages.success(request, _('Profile update success'))

        return redirect('dashboard:admin_profile_details')


# Render AdminProfileSettings view
class AdminProfileSettingsView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/profile_settings.html'
