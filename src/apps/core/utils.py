from django.core.mail import send_mail as _send_email_django
from django.utils.translation import gettext as _
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django_q.tasks import async_task
import datetime
import requests
import string
import random
import json
import re


def random_str(size=15, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_num(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_time(frmt='%Y-%m-%d_%H:%M'):
    t = timezone.now()
    if frmt is not None:
        t = t.strftime(frmt)
    return t


def get_timesince_persian(time):
    time_server = get_time(None)

    diff_time = datetime.datetime(time_server.year, time_server.month, time_server.day, time_server.hour,
                                  time_server.minute) - datetime.datetime(time.year, time.month, time.day, time.hour,
                                                                          time.minute)

    diff_time_sec = diff_time.total_seconds()
    # sec = diff_time_sec % 60
    min = int(diff_time_sec // 60 % 60)
    hour = int(diff_time_sec // 3600)
    day = diff_time.days
    result = ''
    if min > 0:
        result = f'{min} دقیقه پیش'
    else:
        result = f'لحظاتی پیش'

    if hour > 0:
        result = f'{hour} ساعت پیش'

    if day > 0:
        result = f'{day}  روز پیش'

    return result


def send_sms(phonenumber, pattern_code, values={}):
    phonenumber = str(phonenumber).replace('+', '')
    payload = json.dumps({
        "pattern_code": pattern_code,
        "originator": settings.SMS_CONFIG['ORIGINATOR'],
        "recipient": phonenumber,
        "values": values
    })
    headers = {
        'Authorization': "AccessKey {}".format(settings.SMS_CONFIG['API_KEY']),
        'Content-Type': 'application/json'
    }

    async_task(
        requests.request,
        'POST',
        settings.SMS_CONFIG['API_URL'],
        headers=headers,
        data=payload
    )


def send_email(email, subject, content, **kwargs):
    # send email in background
    async_task(_send_email_django,
               subject,
               content,
               settings.EMAIL_HOST_USER,
               [email]
               )


# Check phone number format(IR)
def check_phone_number(number):
    mobile_regex = "^09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$"
    try:
        number = str(number)
        print(number)
        if number and re.search(mobile_regex, number):
            return True
    except (TypeError, NameError):
        pass

    return False


def add_prefix_phonenum(phonenumber):
    phonenumber = str(phonenumber).replace('+98', '')
    return f'+98{phonenumber}'


def get_raw_phonenum(phonenumber):
    p = str(phonenumber).replace('+98', '')
    return p


def normalize_phone(phonenumber):
    try:
        if phonenumber[0] == '0':
            phonenumber = str(phonenumber).replace('0', '+98', 1)
    except (TypeError, IndexError):
        pass

    return phonenumber


def form_validate_err(request, form):
    if form.is_valid() is False:
        errors = form.errors.as_data()
        if errors:
            for field, err in errors.items():
                err = str(err[0])
                err = err.replace('[', '').replace(']', '')
                err = err.replace("'", '').replace('This', '')
                err = f'{field} {err}'
                messages.error(request, err)
        else:
            messages.error(request, 'دیتای ورودی نامعتبر است')
        return False
    return True


# Message form errors utils
def message_form_errors(request, form):
    errors = form.errors.items()
    if not errors:
        messages.error(request, _('Entered data is not correct.'))
        return False

    for field, message in errors:
        for error in message:
            messages.error(request, error)


def get_host_url(url):
    return settings.HOST_ADDRESS + url


def get_media_url(url):
    return settings.MEDIA_URL + url



