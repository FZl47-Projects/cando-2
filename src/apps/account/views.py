from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from django.db.models import Value, Q
from django.views.generic import View
from django.contrib import messages
from django.core import serializers
from django.conf import settings

from apps.core.utils import add_prefix_phonenum, random_num, form_validate_err
from apps.core.redis_py import set_value_expire, remove_key, get_value
from apps.core.auth.mixins import LoginRequiredMixinCustom
from apps.core.auth.decorators import admin_required_cbv
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

        return redirect('dashboard:index')

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


class UserAdd(View):
    template_name = 'account/dashboard/user/add.html'

    @admin_required_cbv()
    def get(self, request):
        context = {
            'buildings': Building.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)

    @admin_required_cbv()
    def post(self, request):
        data = request.POST.copy()
        # create user
        f = forms.RegisterUserFullForm(data=data)
        if form_validate_err(request, f) is False:
            return redirect('account:user_add')
        user = f.save()
        user.is_active = True
        user.set_password(f.cleaned_data['password2'])
        user.save()
        # set building avaialable
        data['user'] = user
        building_available = BuildingAvailable.get_or_create_building_user(user)
        f = forms.SetBuildingAvailable(data=data, instance=building_available)
        if f.is_valid():
            f.save()
        # create notif for admin
        NotificationUser.objects.create(
            type='CREATE_USER_BY_ADMIN',
            to_user=request.user,
            title='ایجاد کاربر توسط ادمین',
            description=f"""
                    کاربر {user.phonenumber}
                    ایجاد شد
                """,
            is_showing=False
        )
        messages.success(request, 'حساب کاربر با موفقیت ایجاد شد')
        return redirect(user.get_absolute_url())


class UserDetail(LoginRequiredMixinCustom, View):

    def get_template(self, user_obj):
        if user_obj.is_common_admin:
            return 'account/dashboard/admin/detail.html'
        else:
            return 'account/dashboard/user/detail.html'

    @admin_required_cbv()
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        # ony super admin can access to admin detail
        if user.is_common_admin and request.user.is_super_admin is False:
            raise Http404
        # super user detail cant be accessible
        if user.is_super_admin:
            raise Http404
        context = {
            # name 'user_detail' for prevent conflict
            'user_detail': user,
            'buildings_user': Building.get_buildings_user(user),
            'buildings': Building.objects.filter(is_active=True),
        }

        if user.is_common_admin:
            context['receipt_tasks'] = ReceiptTask.objects.filter(user_admin=user)

        return render(request, self.get_template(user), context)


class UserDetailDelete(LoginRequiredMixinCustom, View):

    @admin_required_cbv(['super_user'])
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.is_super_admin:
            messages.error(request, 'شما نمیتوانید کاربر ویژه را حذف کنید')
            return redirect('account:user_list')
        user.delete()
        messages.success(request, 'کاربر با موفقیت حذف شد')
        return redirect('account:user_list')


class UserUpdate(LoginRequiredMixinCustom, View):

    def post(self, request):
        user = request.user
        data = request.POST
        f = forms.UpdateUserForm(instance=user, data=data)
        if form_validate_err(request, f) is False:
            return redirect('account:info_detail')
        f.save()
        messages.success(request, 'مشخصات شما با موفقیت بروزرسانی شد')
        return redirect('account:info_detail')


class UserUpdatePassword(LoginRequiredMixinCustom, View):

    def post(self, request):
        user = request.user
        data = request.POST
        f = forms.UpdateUserPassword(data=data)
        if form_validate_err(request, f) is False:
            return redirect('account:info_change_password')
        data = f.cleaned_data
        if not user.check_password(data['current_password']):
            messages.error(request, 'رمز عبور فعلی نادرست است')
            return redirect('account:info_change_password')
        user.set_password(data['new_password'])
        user.save()
        messages.success(request, 'رمز عبور شما با موفقیت بروزرسانی شد')
        return redirect('account:login_register')


class UserList(View):
    template_name = 'account/dashboard/user/list.html'

    def search(self, request, objects):
        s = request.GET.get('search')
        if not s:
            return objects
        objects = objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
        lookup = Q(phonenumber__icontains=s) | Q(full_name__icontains=s) | Q(
            email__icontains=s)
        return objects.filter(lookup)

    @admin_required_cbv()
    def get(self, request):
        users = User.normal_user.all()
        users = self.search(request, users)
        page_num = request.GET.get('page', 1)
        pagination = Paginator(users, 20)
        pagination = pagination.get_page(page_num)
        users = pagination.object_list
        context = {
            'users': users,
            'pagination': pagination
        }
        return render(request, self.template_name, context)


class UserListComponentPartial(View):
    template_name = 'account/dashboard/user/components/list.html'

    @admin_required_cbv()
    def get(self, request):
        users = User.normal_user.all()
        page_num = request.GET.get('page', 1)
        pagination = Paginator(users, 20)
        pagination = pagination.get_page(page_num)
        users = pagination.object_list
        context = {
            'users': users,
            'pagination': pagination
        }
        return render(request, self.template_name, context)

    @admin_required_cbv()
    def post(self, request):
        data = json.loads(request.body)

        def search(self, objects):
            s = data.get('search')
            if not s:
                return objects
            objects = objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            lookup = Q(phonenumber__icontains=s) | Q(full_name__icontains=s) | Q(
                email__icontains=s)
            return objects.filter(lookup)

        # ajax view
        if not request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
            raise Http404
        users = User.normal_user.all()
        users = search(request, users)
        users_serialized = serializers.serialize('json', users, fields=('id', 'first_name', 'last_name', 'email', 'phonenumber'))
        return JsonResponse(users_serialized, safe=False)
