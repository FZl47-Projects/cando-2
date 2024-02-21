from persiantools.jdatetime import JalaliDate
from datetime import datetime
from django import template

register = template.Library()


@register.filter
def convert_date(value):
    if value:
        value = datetime.strptime(value, '%Y-%m-%d')
        return JalaliDate.to_jalali(value)
    return ''
