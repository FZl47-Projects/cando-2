import datetime
from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'initial and create tasks'

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        midnight = datetime.datetime(year=now.year, month=now.month, day=now.day) + datetime.timedelta(days=1)
        Schedule.objects.create(
            func='apps.product.tasks.deactivation_of_showcase_products',
            repeats=-1,  # infinite
            schedule_type=Schedule.DAILY,
            next_run=midnight
        )
