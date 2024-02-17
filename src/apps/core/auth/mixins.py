from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class LoginRequiredMixinCustom(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_phonenumber_confirmed:
            return redirect('account:confirm_phonenumber')
        
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    """ Admin users access only """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('account:login_register')

        if not request.user.is_admin:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
