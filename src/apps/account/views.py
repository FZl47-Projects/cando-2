from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.views.generic import View
from django.contrib import messages
from django.conf import settings

from apps.core.utils import add_prefix_phonenum, random_num, form_validate_err
from apps.core.redis_py import set_value_expire, remove_key, get_value
from apps.core.auth.mixins import LoginRequiredMixinCustom
from apps.notification.models import NotificationUser
from apps.account import forms
import json

User = get_user_model()
RESET_PASSWORD_CONFIG = settings.RESET_PASSWORD_CONFIG
CONFIRM_PHONENUMBER_CONFIG = settings.CONFIRM_PHONENUMBER_CONFIG


def login_register(request):
    def login_perform(data):
        phonenumber = data.get('phonenumber', None)
        password = data.get('password', None)

        if not (phonenumber or password):
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:login_register')

        # Authenticate user
        phonenumber = add_prefix_phonenum(phonenumber)
        user = authenticate(request, username=phonenumber, password=password)

        if user is None:
            messages.error(request, 'کاربری با این مشخصات یافت نشد!')
            return redirect('account:login_register')
        elif user.is_active is False:
            messages.error(request, 'حساب شما غیر فعال میباشد')
            return redirect('account:login_register')

        # Login user
        login(request, user)
        messages.success(request, 'خوش امدید')

        # Redirect to url or dashboard
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)

        return redirect('public:home')

    def register_perform(data):
        form = forms.RegisterUserForm(data=data)
        if form.is_valid() is False:
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:login_register')

        phonenumber = form.cleaned_data['phonenumber']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']

        # Check for exists normal_user
        if User.objects.filter(phonenumber=phonenumber).exists():
            messages.error(request, 'کاربری با این شماره از قبل ثبت شده است')
            return redirect('account:login_register')

        # Create user
        password = form.cleaned_data['password2']
        user = User(
            phonenumber=phonenumber,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        user.set_password(password)
        user.save()

        # Login user
        login(request, user)
        messages.success(request, 'حساب شما با موفقیت ایجاد شد پس از تایید شماره همراه حساب شما فعال میشود')

        return redirect('account:confirm_phonenumber')

    if request.method == 'GET':
        return render(request, 'account/login-register.html')

    elif request.method == 'POST':
        data = request.POST
        type_page = data.get('type-page', 'login')

        if type_page == 'login':
            return login_perform(data)
        elif type_page == 'register':
            return register_perform(data)


def reset_password(request):
    return render(request, 'account/reset-password.html')


@require_POST
def reset_password_send(request):
    # AJAX view
    data = json.loads(request.body)
    phonenumber = data.get('phonenumber', None)
    # validate data
    if not phonenumber:
        return HttpResponseBadRequest()
    # check user is exists
    try:
        phonenumber = add_prefix_phonenum(phonenumber)
        user = User.objects.get(phonenumber=phonenumber)
    except:
        raise Http404
    code = random_num(RESET_PASSWORD_CONFIG['CODE_LENGTH'])
    key = RESET_PASSWORD_CONFIG['STORE_BY'].format(phonenumber)
    # check code state set
    if get_value(key) is not None:
        # code is already set
        return HttpResponse(status=409)
    # set code
    set_value_expire(key, code, RESET_PASSWORD_CONFIG['TIMEOUT'])
    # send code
    NotificationUser.objects.create(
        type='RESET_PASSWORD_CODE_SENT',
        kwargs={
            'code': code
        },
        to_user=user,
        title='بازیابی رمز عبور',
        description=f"""  کد بازیابی رمز عبور : {code}""",
        send_notify=True
    )
    return JsonResponse({})


@require_POST
def reset_password_check(request):
    # AJAX view
    data = json.loads(request.body)
    phonenumber = data.get('phonenumber', None)
    code = data.get('code', None)
    # validate data
    if (not code) or (not phonenumber):
        return HttpResponseBadRequest()
    phonenumber = add_prefix_phonenum(phonenumber)
    key = RESET_PASSWORD_CONFIG['STORE_BY'].format(phonenumber)
    # check code
    code_stored = get_value(key)
    if code_stored is None:
        # code is not seted or timeout
        return HttpResponse(status=410)
    if code_stored != code:
        # code is wrong(not same)
        return HttpResponse(status=409)
    return JsonResponse({})


@require_POST
def reset_password_set(request):
    # AJAX view
    data = json.loads(request.body)
    f = forms.ResetPasswordSetForm(data)
    # validate data
    if f.is_valid() is False:
        return HttpResponseBadRequest()
    clean_data = f.cleaned_data
    # phonenumber must get from data (not clean_data)
    phonenumber = data['phonenumber']
    code = clean_data['code']
    password = clean_data['password2']
    # check user is exists
    try:
        phonenumber = add_prefix_phonenum(phonenumber)
        user = User.objects.get(phonenumber=phonenumber)
    except:
        raise Http404
    key = RESET_PASSWORD_CONFIG['STORE_BY'].format(phonenumber)
    # check code
    code_stored = get_value(key)
    if code_stored is None:
        # code is not seted or timeout
        return HttpResponse(status=410)
    if code_stored != code:
        # code is wrong(not same)
        return HttpResponse(status=409)
    user.set_password(password)
    user.save()
    remove_key(key)
    NotificationUser.objects.create(
        type='PASSWORD_CHANGED_SUCCESSFULLY',
        to_user=user,
        title='رمز عبور شما تغییر کرد',
        description="""رمز عبور شما با موفقیت تغییر کرد""",
        send_notify=True
    )
    return JsonResponse({})


class ConfirmPhoneNumber(LoginRequiredMixin, View):
    template_name = 'account/confirm-phonenumber.html'

    def get(self, request):
        user = request.user
        if user.is_phonenumber_confirmed:
            return redirect('dashboard:index')
        key = CONFIRM_PHONENUMBER_CONFIG['STORE_BY'].format(user.get_raw_phonenumber())
        context = {
            'code_is_sent': bool(get_value(key))
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # AJAX view
        user = request.user
        code = random_num(CONFIRM_PHONENUMBER_CONFIG['CODE_LENGTH'])
        key = CONFIRM_PHONENUMBER_CONFIG['STORE_BY'].format(user.get_raw_phonenumber())
        # check code state set
        if get_value(key) is not None:
            # code is already set
            return HttpResponse(status=409)
        # set code
        set_value_expire(key, code, CONFIRM_PHONENUMBER_CONFIG['TIMEOUT'])
        # send code
        NotificationUser.objects.create(
            type='CONFIRM_PHONENUMBER_CODE_SENT',
            kwargs={
                'code': code
            },
            to_user=user,
            title='کد تایید شماره همراه',
            description=f""" کد تایید شماره همراه : {code}""",
            send_notify=True
        )
        return JsonResponse({})


class ConfirmPhoneNumberCheckCode(LoginRequiredMixin, View):

    def post(self, request):
        # AJAX view
        data = json.loads(request.body)
        code = data.get('code', None)
        # validate data
        if not code:
            return HttpResponseBadRequest()
        user = request.user
        key = CONFIRM_PHONENUMBER_CONFIG['STORE_BY'].format(user.get_raw_phonenumber())
        # check code
        code_stored = get_value(key)
        if code_stored is None:
            # code is not seted or timeout
            return HttpResponse(status=410)
        if code_stored != code:
            # code is wrong(not same)
            return HttpResponse(status=409)
        # confirm phonenumber
        user.is_phonenumber_confirmed = True
        user.save()
        NotificationUser.objects.create(
            type='PHONENUMBER_CONFIRMED',
            to_user=user,
            title='شماره همراه تایید شد',
            description=f"شماره همراه کاربر با موفقیت تایید شد",
            send_notify=True
        )
        messages.success(request, 'شماره همراه شما تایید شد')
        return JsonResponse({})


class DashboardInfoDetail(LoginRequiredMixinCustom, View):

    def get(self, request):
        return render(request, 'account/dashboard/information/detail.html')


class DashboardInfoChangePassword(LoginRequiredMixinCustom, View):

    def get(self, request):
        return render(request, 'account/dashboard/information/change-password.html')


# UpdatePassword view
class UpdatePasswordView(LoginRequiredMixinCustom, View):
    def get_referer_url(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        return referer_url

    def post(self, request):
        user = request.user
        password = request.POST.get('password')

        if not user.check_password(password):
            messages.error(request, _('Password is not correct'))
            return redirect(self.get_referer_url(request) or '/')

        password2 = request.POST.get('password2')
        user.set_password(password2)
        user.save()

        messages.success(request, _('Password successfully changed'))
        return redirect(self.get_referer_url(request) or '/')
