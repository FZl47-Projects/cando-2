from django.utils.translation import gettext as _
from django.db.models import TextChoices


# UserRoles enum
class UserRolesEnum(TextChoices):
    NORMAL = 'normal_user', _('Normal user')
    OPERATOR = 'operator_user', _('Operator user')
    SUPER = 'super_user', _('Super user')


# UserGenders enum
class UserGendersEnum(TextChoices):
    UNKNOWN = 'unknown', _('Unknown')
    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')
