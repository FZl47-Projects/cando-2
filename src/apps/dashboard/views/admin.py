from django.views.generic import View, TemplateView, DetailView, ListView
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

from apps.core.utils import form_validate_err, normalize_phone
from apps.core.auth.mixins import AdminRequiredMixin
from apps.account.models import User
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


# Render UsersList view
class UsersListView(AdminRequiredMixin, ListView):
    template_name = 'dashboard/admin/users_list.html'
    model = User
    paginate_by = 40

    # TODO: Add filters

    def search(self, objects):
        q = self.request.GET.get('q')
        if q:
            q = normalize_phone(q)
            objects = objects.filter(Q(phonenumber__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        return objects

    def get_queryset(self):
        queryset = User.objects.all()
        queryset = self.search(queryset)

        return queryset


# Render UserDetails view
class UserDetailsView(AdminRequiredMixin, DetailView):
    template_name = 'dashboard/admin/user_details.html'
    model = User
