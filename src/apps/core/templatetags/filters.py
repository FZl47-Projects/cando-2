from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime
from django import template

register = template.Library()


@register.filter
def convert_date(value):
    if value:
        value = datetime.strptime(value, '%Y-%m-%d')
        return JalaliDate.to_jalali(value)
    return ''


@register.filter
def convert_datetime(value):
    if value:
        return JalaliDateTime.to_jalali(value)
    return ''

