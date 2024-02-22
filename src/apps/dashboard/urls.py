from django.urls import path
from .views import admin, user


app_name = 'apps.dashboard'

urlpatterns = [
    # Admin dashboard url
    path('admin/', admin.AdminDashboardView.as_view(), name='admin'),
    path('admin/profile/', admin.AdminProfileView.as_view(), name='admin_profile_details'),
    path('admin/profile/settings/', admin.AdminProfileSettingsView.as_view(), name='admin_profile_settings'),
    path('admin/users/list/', admin.UsersListView.as_view(), name='admin_users_list'),
    path('admin/user/<int:pk>/', admin.UserDetailsView.as_view(), name='admin_user_details'),
    path('admin/user/add/', admin.AddUserView.as_view(), name='admin_add_user'),
    path('admin/user/delete/', admin.DeleteUserView.as_view(), name='admin_delete_user'),
    path('admin/user/<int:pk>/disable/', admin.DisableUserView.as_view(), name='admin_disable_user'),

    # User dashboard urls
    path('', user.Index.as_view(), name='user'),
]
