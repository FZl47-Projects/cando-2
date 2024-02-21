from django.urls import path
from .views import admin, user


app_name = 'apps.dashboard'

urlpatterns = [
    path('admin/', admin.AdminDashboardView.as_view(), name='admin'),
    path('admin/profile/', admin.AdminProfileView.as_view(), name='admin_profile_details'),
    path('admin/profile/settings/', admin.AdminProfileSettingsView.as_view(), name='admin_profile_settings'),
    path('', user.Index.as_view(), name='user'),
]
