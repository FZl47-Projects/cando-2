from django.urls import path
from .views import admin, user


app_name = 'apps.dashboard'

urlpatterns = [
    path('admin/', admin.AdminDashboardView.as_view(), name='admin'),
    path('', user.Index.as_view(), name='user'),
]
