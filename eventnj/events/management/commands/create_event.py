from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Event, Organizer
from datetime import datetime
from random import choice, randint


# from django.conf import settings
# from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "wypełnij organizer danymi -- python manage.py create_event 1"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of organizers to be created')

    def handle(self, *args, **options):
        total = options['total']

        # len_events = len(Event.objects.all())

        # sprawdzaj jaki postfix ma ostatni rekord
        # ostatni = Event.objects.all()[len_events - 1:len_events].get().id
        ostatni = Event.objects.last().id

        # postfix kolejnej wartości
        # https://docs.python.org/3.9/library/string.html
        # postfix = "{:0>5}".format(str(ostatni + 1))

        formatedDate = datetime.now(tz=timezone.utc)

        # myDate = datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)

        # formatedDate = myDate #.strftime("%Y-%m-%d %H:%M:%S")
        CONST_RANDINT_RESERVE = 25
        CONST_RANDINT = 50
        CONST_PRICE = 25

        for i in range(total):
            postfix = str("{:0>5}".format(str(ostatni + 1 + i)))
            # print(postfix)
            Event.objects.create(
                title="event_" + postfix,
                description="description_" + postfix,
                limit_participant_reserve=CONST_RANDINT_RESERVE + randint(1, 3) * 10,
                limit_participant=CONST_RANDINT + randint(1, 6) * 10,
                start=formatedDate,
                end=formatedDate,
                start_registration=formatedDate,
                end_registration=formatedDate,
                country="country_" + postfix,
                city="city_" + postfix,
                street="street_" + postfix,
                postcode=postfix,
                room="room_" + postfix,
                price=CONST_PRICE + randint(1, 10) * 5,
                is_online=False,
                online_link="link_" + postfix,
            )

        self.stdout.write(self.style.SUCCESS(f"dopisane {total} rekordów"))
