from django.utils.translation import gettext as _
from django.contrib import admin
from .models import UserNote


# Register UserNotes admin
@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_phone', 'author')
    list_display_links = ('id', 'get_phone')
    list_filter = ('is_active',)

    @admin.display(description=_('Phone number'))
    def get_phone(self, obj):
        return obj.user.get_phone_number()

    @admin.display(description=_('Name'))
    def get_name(self, obj):
        return obj.user.get_full_name()
