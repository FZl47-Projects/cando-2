from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserProfile


# Unregister Groups
admin.site.unregister(Group)


# Register Custom user admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ('get_phone_number',  'is_active', 'is_staff', 'is_superuser', 'is_phonenumber_confirmed', 'last_login', 'role')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'role',)
    fieldsets = (
        (None, {'fields': ('phonenumber', 'password', 'role', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_phonenumber_confirmed', 'user_permissions')}),
        (_('Dates'), {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phonenumber', 'password1', 'password2', 'is_staff', 'is_active', 'is_phonenumber_confirmed', 'first_name', 'last_name'
            )
        }),
    )
    search_fields = ('phonenumber',)
    ordering = ('phonenumber',)

    @admin.display(description=_('Phone number'))
    def get_phone_number(self, obj):
        if obj.id:
            return str(obj.phonenumber).replace('+98', '0')


# Register UserProfile admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_phone_number', 'gender', 'melli_code']
    list_display_links = ['id', 'get_phone_number']
    list_filter = ['gender']
    search_fields = ['user__phonenumber']

    @admin.display(description=_('Phone number'))
    def get_phone_number(self, obj):
        if obj.id:
            return str(obj.user.phonenumber).replace('+98', '0')
