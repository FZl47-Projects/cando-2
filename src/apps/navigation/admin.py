from django.utils.translation import gettext as _
from django.contrib import admin
from .models import Address


# Register Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_phone_number', 'province', 'city', 'active')
    list_display_links = ('id', 'get_phone_number')
    list_filter = ('active',)

    @admin.display(description=_('Phone number'))
    def get_phone_number(self, obj):
        if obj.id:
            return str(obj.user.get_phone_number())
