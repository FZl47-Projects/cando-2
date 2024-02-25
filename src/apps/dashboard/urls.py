from django.urls import path
from . import views


app_name = 'apps.dashboard'

urlpatterns = [
    # Admin dashboard urls
    path('admin/', views.AdminDashboardView.as_view(), name='admin'),
    path('admin/profile/', views.AdminProfileView.as_view(), name='admin_profile_details'),
    path('admin/profile/settings/', views.AdminProfileSettingsView.as_view(), name='admin_profile_settings'),
    path('admin/users/list/', views.UsersListView.as_view(), name='admin_users_list'),
    path('admin/user/<int:pk>/', views.UserDetailsView.as_view(), name='admin_user_details'),
    path('admin/user/add/', views.AddUserView.as_view(), name='admin_add_user'),
    path('admin/user/delete/', views.DeleteUserView.as_view(), name='admin_delete_user'),
    path('admin/user/<int:pk>/disable/', views.DisableUserView.as_view(), name='admin_disable_user'),
    path('admin/user/note/add/', views.AddUserNoteView.as_view(), name='admin_add_note'),
    path('admin/user/note/<int:pk>/del/', views.DeleteUserNoteView.as_view(), name='admin_delete_note'),

    path('admin/products/', views.ProductListView.as_view(), name='admin_products'),
]
