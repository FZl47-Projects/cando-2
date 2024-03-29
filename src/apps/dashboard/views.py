from django.views.generic import View, TemplateView, DetailView, ListView, FormView
from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from apps.core.utils import form_validate_err, message_form_errors, normalize_phone
from apps.account.forms import UpdateProfileForm, AddUserForm
from apps.core.auth.mixins import AdminRequiredMixin
from apps.product import models as product_models
from apps.account.models import User
from .models import UserNote
from . import forms


# Render AdminDashboard view
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/index.html'


# Render AdminProfile view
class AdminProfileView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/profile_details.html'

    def post(self, request):
        form = UpdateProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)

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
    context_object_name = 'object'


# AddUser view
class AddUserView(AdminRequiredMixin, FormView):
    template_name = 'dashboard/admin/users_list.html'
    form_class = AddUserForm
    success_url = reverse_lazy('dashboard:admin_users_list')
    
    def form_valid(self, form):
        form.save(commit=False)
        messages.success(self.request, _('User successfully added'))
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        message_form_errors(self.request, form)
        return redirect('dashboard:admin_users_list')


# DeleteUser view
class DeleteUserView(AdminRequiredMixin, View):
    def post(self, request):
        user_id = request.POST.get('id')
        user = get_object_or_404(User, id=user_id)
        user.delete()

        messages.success(request, _('User successfully deleted'))
        return redirect('dashboard:admin_users_list')


# DisableUser view
class DisableUserView(AdminRequiredMixin, View):
    def get(self, request, pk):
        try:
            obj = User.objects.get(id=pk)
            obj.is_active = not obj.is_active
            obj.save()

            return JsonResponse({'disable': obj.is_active})
        except User.DoesNotExist:
            pass

        return JsonResponse({'disable': False})


# Add UserNote view
class AddUserNoteView(AdminRequiredMixin, FormView):
    template_name = 'dashboard/admin/user_details.html'
    form_class = forms.AddUserNoteForm

    def get_success_url(self):
        pk = self.request.POST.get('user')
        return reverse('dashboard:admin_user_details', args=[pk])

    def get_form(self, form_class=None):
        data = self.request.POST.copy()
        data.update({
            'author': self.request.user,
        })

        form_class = forms.AddUserNoteForm(data=data)
        return form_class

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('There is an issue. please try again'))
        return super().get_success_url()


# Delete UserNote view
class DeleteUserNoteView(AdminRequiredMixin, View):
    def get(self, request, pk):
        try:
            obj = UserNote.objects.get(pk=pk)
            obj.delete()
        except UserNote.DoesNotExist:
            messages.error(request, _('There is an issue. please try again'))

        referer_url = request.META.get('HTTP_REFERER')
        return redirect(referer_url or reverse('dashboard:admin_users_list'))


# Render ProductList view
class ProductListView(AdminRequiredMixin, ListView):
    template_name = 'dashboard/admin/products.html'
    model = product_models.CakeProduct
    paginate_by = 20

    def get_queryset(self):
        queryset = product_models.CakeProduct.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# Create CakeProduct view
# class CreateCakeProductView(AdminRequiredMixin, View):
#     def post(self, request):

