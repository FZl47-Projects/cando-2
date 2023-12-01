from django.urls import path
from .views import dashboard

app_name = 'apps.account'
urlpatterns = [
    # login logout and register
    path('login-register', dashboard.login_register, name='login_register'),
    path('logout', dashboard.Logout.as_view(), name='logout'),
    # confirm account
    path('confirm/phonenumber', dashboard.ConfirmPhonenumber.as_view(), name='confirm_phonenumber'),
    path('confirm/phonenumber/check', dashboard.ConfirmPhonenumberCheckCode.as_view(),
         name='confirm_phonenumber_check_code'),
    # reset password
    path('reset-password', dashboard.reset_password, name='reset_password'),
    path('reset-password/send-code', dashboard.reset_password_send, name='reset_password_send_code'),
    path('reset-password/check-code', dashboard.reset_password_check, name='reset_password_check_code'),
    path('reset-password/set', dashboard.reset_password_set, name='reset_password_set'),
]
