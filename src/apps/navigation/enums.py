from django.utils.translation import gettext as _
from django.db.models import TextChoices


class DeliveryTime(TextChoices):
    FASTEST = 'fastest', _('Fastest')
    UNTIL_COMPLETED = 'until_completed', _('Until completed')