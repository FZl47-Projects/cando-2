from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class NavigationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.navigation'
    verbose_name = _('Navigation')
