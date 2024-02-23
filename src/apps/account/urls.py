from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


app_name = 'apps.account'

urlpatterns = [
    # Login, logout and register
    path('login-register/', views.login_register, name='login_register'),
    path('logout/', LogoutView.as_view(next_page='public:home'), name='logout'),

    # Confirm account
    path('confirm/phonenumber/', views.ConfirmPhoneNumber.as_view(), name='confirm_phonenumber'),
    path('confirm/phonenumber/check/', views.ConfirmPhoneNumberCheckCode.as_view(), name='confirm_phonenumber_check_code'),

    # Reset password
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-password/send-code/', views.reset_password_send, name='reset_password_send_code'),
    path('reset-password/check-code/', views.reset_password_check, name='reset_password_check_code'),
    path('reset-password/set/', views.reset_password_set, name='reset_password_set'),

    # Profile urls
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Extra things
    path('password/change/', views.UpdatePasswordView.as_view(), name='change_password'),
]
