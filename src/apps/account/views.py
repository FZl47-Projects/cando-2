import json
from django.contrib import messages
from django.conf import settings
from django.db.models import Value, Q
from django.db.models.functions import Concat
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, get_user_model, logout as logout_handler

from apps.core.utils import add_prefix_phonenum, random_num
from apps.core.auth.decorators import admin_required_cbv
from apps.core.redis_py import set_value_expire, remove_key, get_value
from apps.notification.models import NotificationUser
from apps.account import forms
from apps.product.models import Cart, WishList

User = get_user_model()
RESET_PASSWORD_CONFIG = settings.RESET_PASSWORD_CONFIG
CONFIRM_PHONENUMBER_CONFIG = settings.CONFIRM_PHONENUMBER_CONFIG


def login_register(request):
    # TODO: need to refactor

    def set_cart_on_user(user):
        cart_user = user.get_current_cart_or_create()
        cart_session = Cart.get_session_cart(request)
        cart_session.get_products().update(cart=cart_user)
        cart_session.get_custom_products().update(cart=cart_user)
        cart_session.delete()

    def set_wishlist_on_user(user):
        wishlist_user = getattr(user, 'wishlist', None)
        wishlist_session = WishList.get_session_wishlist(request)
        if wishlist_user:
            wishlist_user.products.add(*wishlist_session.products.all())
            wishlist_session.delete()
            return
        wishlist_session.user = user
        wishlist_session.save()

    def login_perform(data):
        phonenumber = data.get('phonenumber', None)
        password = data.get('password', None)
        if not (phonenumber or password):
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:login_register')
        phonenumber = add_prefix_phonenum(phonenumber)
        user = authenticate(request, username=phonenumber, password=password)
        if user is None:
            messages.error(request, 'کاربری با این مشخصات یافت نشد یا حساب غیر فعال میباشد')
            return redirect('account:login_register')
        if user.is_active is False:
            messages.error(request, 'حساب شما غیر فعال میباشد')
            return redirect('account:login_register')
        login(request, user)
        messages.success(request, 'خوش امدید')
        # set session cart and wishlist on user
        set_cart_on_user(user)
        set_wishlist_on_user(user)

        # redirect to url or dashboard
        next_url = request.GET.get('next')
        try:
            # maybe next url not valid
            if next_url:
                return redirect(next_url)
        except:
            pass
        return redirect('dashboard:index')

    def register_perform(data):
        f = forms.RegisterUserForm(data=data)
        if f.is_valid() is False:
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:login_register')
        # check for exists normal_user
        phonenumber = f.cleaned_data['phonenumber']
        first_name = f.cleaned_data['first_name']
        last_name = f.cleaned_data['last_name']
        if User.objects.filter(phonenumber=phonenumber).exists():
            messages.error(request, 'کاربری با این شماره از قبل ثبت شده است')
            return redirect('account:login_register')
        # create user
        password = f.cleaned_data['password2']
        user = User(
            phonenumber=phonenumber,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        user.set_password(password)
        user.save()
        # login
        login(request, user)
        messages.success(request, 'حساب شما با موفقیت ایجاد شد پس از تایید شماره همراه حساب شما فعال میشود')
        # set session cart and wishlist on user
        set_cart_on_user(user)
        set_wishlist_on_user(user)

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


class Logout(View):

    def get(self, request):
        logout_handler(request)
        return redirect('public:home')


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


class ConfirmPhonenumber(LoginRequiredMixin, View):
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


class ConfirmPhonenumberCheckCode(LoginRequiredMixin, View):

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
        users_serialized = serializers.serialize('json', users,
                                                 fields=('id', 'first_name', 'last_name', 'email', 'phonenumber'))
        return JsonResponse(users_serialized, safe=False)
