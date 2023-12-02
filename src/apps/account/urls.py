from django.urls import path
from . import views

app_name = 'apps.account'
urlpatterns = [
    # login logout and register
    path('login-register', views.login_register, name='login_register'),
    path('logout', views.Logout.as_view(), name='logout'),
    # confirm account
    path('confirm/phonenumber', views.ConfirmPhonenumber.as_view(), name='confirm_phonenumber'),
    path('confirm/phonenumber/check', views.ConfirmPhonenumberCheckCode.as_view(),
         name='confirm_phonenumber_check_code'),
    # reset password
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset-password/send-code', views.reset_password_send, name='reset_password_send_code'),
    path('reset-password/check-code', views.reset_password_check, name='reset_password_check_code'),
    path('reset-password/set', views.reset_password_set, name='reset_password_set'),
]
